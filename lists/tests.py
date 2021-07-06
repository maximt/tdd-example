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

    def test_display_onjy_items_for_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Correct item 1', list=correct_list)
        Item.objects.create(text='Correct item 2', list=correct_list)
        
        other_list = List.objects.create()
        Item.objects.create(text='Other item 1', list=other_list)
        Item.objects.create(text='Other item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Correct item 1')
        self.assertContains(response, 'Correct item 2')
        self.assertNotContains(response, 'Other item 1')
        self.assertNotContains(response, 'Other item 2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')
    
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):

    def test_save_post_request(self):
        item_text = 'This is a new item'
        response = self.client.post('/lists/new', data={'item_text': item_text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'This is a new item'})
        
        list_ = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_.id}/')

    def test_can_save_post_request_to_exists_list(self):
        new_item_text = 'A new item for existing list'

        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': new_item_text},
        )

        self.assertEqual(Item.objects.count(), 1)
        item_created = Item.objects.first()

        self.assertEqual(item_created.text, new_item_text)
        self.assertEqual(item_created.list, correct_list)

    def test_redirects_to_list_view(self):
        new_item_text = 'A new item for existing list'

        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': new_item_text},
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

