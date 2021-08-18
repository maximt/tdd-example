## Requirements:
* nginx
* python 3.6
* virtualenv 
* pip
* git

sudo apt-get install nginx git python3 python3-venv

## Create nginx site 
* nginx.template.conf
* Replace SITENAME

## systemd
* gunicorn-systemd.template.service
* Replace SITENAME
* Replace ENVFILE

## Dirs
    /home/username
    └─sites
        └─SITENAME
            ├─ database
            ├─ source
            ├─ static
            └─ virtualenv
