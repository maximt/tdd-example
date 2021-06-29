from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item 


class HomePageTest(TestCase):

    def test_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_save_post_request(self):
        item_text = 'This is a new item'
        response = self.client.post('/', data={'item_text': item_text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirect_after_post(self):
        response = self.client.post('/', data={'item_text': 'This is a new item'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['location'], '/')

    def test_save_only_non_empty(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
    
    def test_display_list_items(self):
        Item.objects.create(text='Item 1')
        Item.objects.create(text='Item 2')
        
        response = self.client.get('/')

        self.assertIn('Item 1', response.content.decode())
        self.assertIn('Item 2', response.content.decode())



class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        item1 = Item()
        item1.text = 'My first item'
        item1.save()

        item2 = Item()
        item2.text = 'My second item'
        item2.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, 'My first item')
        self.assertEqual(saved_items[1].text, 'My second item')
   
