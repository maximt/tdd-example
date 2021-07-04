from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        item1 = Item()
        item1.text = 'My first item'
        item1.list = list_
        item1.save()

        item2 = Item()
        item2.text = 'My second item'
        item2.list = list_
        item2.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        saved_item1 = saved_items[0]
        saved_item2 = saved_items[1]

        self.assertEqual(saved_item1.text, 'My first item')
        self.assertEqual(saved_item1.list, list_)
        self.assertEqual(saved_item2.text, 'My second item')
        self.assertEqual(saved_item2.list, list_)
   
class ListViewTest(TestCase):

    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='Item 1', list=list_)
        Item.objects.create(text='Item 2', list=list_)
        
        response = self.client.get('/lists/my-single-list/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/my-single-list/')
        self.assertTemplateUsed(response, 'list.html')

class NewListTest(TestCase):

    def test_save_post_request(self):
        item_text = 'This is a new item'
        response = self.client.post('/lists/new', data={'item_text': item_text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'This is a new item'})
        
        self.assertRedirects(response, '/lists/my-single-list/')
