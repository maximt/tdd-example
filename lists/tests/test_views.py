import unittest
from django.test import TestCase
from django.utils.html import escape
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from unittest.mock import patch, Mock
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, MSG_EMPTY_ITEM_ERROR, MSG_DUPLICATE_ITEM_ERROR
from lists.views import new_list


User = get_user_model()


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )

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
        text = 'A new item for existing list'

        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': text},
        )

        self.assertEqual(Item.objects.count(), 1)
        item_created = Item.objects.first()

        self.assertEqual(item_created.text, text)
        self.assertEqual(item_created.list, correct_list)

    def test_redirects_to_list_view(self):
        new_text = 'A new item for existing list'

        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': new_text},
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_show_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(MSG_EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='hello')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'hello'}
        )

        expected_error = escape(MSG_DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')


class NewListViewIntegratedTest(TestCase):

    def test_save_post_request(self):
        text = 'This is a new item'
        response = self.client.post('/lists/new', data={'text': text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertContains(response, escape(MSG_EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='test@test.test')
        self.client.force_login(user)
        self.client.post('/lists/new', data={'text': 'new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):

    def setUp(self) -> None:
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    @patch('lists.views.redirect')
    def test_passes_POST_data_toNewListForm(self, mock_redirect, mockNewListForm):
        new_list(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    @patch('lists.views.redirect')
    def test_saves_form_with_owner_if_form_valid(self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(self.request, 'home.html', {'form': mock_form})

    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)



class MyListsTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='test@test.test')
        response = self.client.get('/lists/users/test@test.test/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='test2@test.test')
        user_correct = User.objects.create(email='test@test.test')
        response = self.client.get('/lists/users/test@test.test/')
        self.assertEqual(response.context['owner'], user_correct)

