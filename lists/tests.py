from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_to_home_page(self):
        view = resolve('/')
        self.assertEqual(view.func, home_page)

