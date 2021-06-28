from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_to_home_page(self):
        view = resolve('/')
        self.assertEqual(view.func, home_page)

    def test_home_page_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))