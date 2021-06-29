from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_to_home_page(self):
        view = resolve('/')
        self.assertEqual(view.func, home_page)

    def test_home_page_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        html_tmpl = render_to_string('home.html')
        self.assertEqual(html, html_tmpl)