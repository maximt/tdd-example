from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List

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


    def test_cannot_save_empty_list_items(self):
       list_ = List.objects.create()
       item = Item(list=list_, text='')

       with self.assertRaises(ValidationError):
           item.full_clean()
           item.save()
        
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')