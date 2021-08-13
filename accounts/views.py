from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from django.urls import reverse
from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url_path = reverse('login') + '?token=' + str(token.uid)
    url = request.build_absolute_uri(url_path)
    body_msg = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        body_msg,
        'vbmax@ya.ru',
        [email],
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
