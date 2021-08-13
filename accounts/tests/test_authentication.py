from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import request
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token


User = get_user_model()


class AuthenticationTest(TestCase):

    def test_returns_none_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(request, uid='no-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = 'test@test.test'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(request, uid=token.uid)
        user_new = User.objects.get(email=email)
        self.assertEqual(user, user_new)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = 'test@test.test'
        user_existing = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(request, uid=token.uid)
        self.assertEqual(user, user_existing)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email='hello@test.test')
        user_desired = User.objects.create(email='test@test.test')
        user_found = PasswordlessAuthenticationBackend().get_user('test@test.test')
        self.assertEqual(user_found, user_desired)

    def test_returns_none_if_no_user_with_that_email(self):
        user_found = PasswordlessAuthenticationBackend().get_user('no@test.test')
        self.assertIsNone(user_found)
