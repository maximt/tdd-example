from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/maximt/tdd-example.git'

def deploy():
    site_dir = f'/home/{env.user}/sites/{env.host}'
    src_dir = site_dir + '/source'
    _create_directory_structure_if_necessary(site_dir)
    _get_latest_source(src_dir)
    _update_settings(src_dir, env.host)
    _update_virtualenv(src_dir)
    _update_static_files(src_dir)
    _update_database(src_dir)

def _create_directory_structure_if_necessary(site_dir):
    for subdir in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_dir}/{subdir}')

def _get_latest_source(src_dir):
    if exists(src_dir + '/.git'):
        run(f'cd {src_dir} && git fetch')
    else:
        run(f'git clone {REPO_URL} {src_dir}')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {src_dir} && git reset --hard {current_commit}')

def _update_settings(src_dir, site_name):
    settings_path = src_dir + '/superlists/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    secret_key_file = src_dir + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(settings_path, f'SECRET_KEY = "{key}"')
    append(settings_path, "\nfrom .secret_key import SECRET_KEY")

def _update_virtualenv(src_dir):
    virtualenv_dir = src_dir + '/../virtualenv'
    pip_path = virtualenv_dir + '/bin/pip'
    if not exists(pip_path):
        run(f'python3 -m venv {virtualenv_dir}')
    run(f'{pip_path} install -r {src_dir}/requirements.txt')

def _update_static_files(src_dir):
    run(f'cd {src_dir} && ../virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database(src_dir):
    run(f'cd {src_dir} && ../virtualenv/bin/python manage.py migrate --noinput')
    