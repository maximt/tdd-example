from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page


class HomePageTest(TestCase):

    def test_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_request(self):
        item_text = 'This is a new item'
        response = self.client.post('/', data={'item_text': item_text})
        self.assertIn(item_text, response.content.decode())
        self.assertTemplateUsed(response, 'home.html')