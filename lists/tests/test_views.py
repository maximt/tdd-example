from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListViewTest(TestCase):

    def test_display_only_items_for_list(self):
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

    def test_can_save_post_request_to_exists_list(self):
        new_item_text = 'A new item for existing list'

        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            f'/lists/{correct_list.id}/',
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
            f'/lists/{correct_list.id}/',
            data={'item_text': new_item_text},
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/',
            data={'item_text':''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have empty list item")
        self.assertContains(response, expected_error)


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

    def test_validation_errors_are_sent_back_to_home_page_tmpl(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        expect_msg = escape("You can't have empty list item")
        self.assertContains(response, expect_msg)

    def test_invalid_items_are_not_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
