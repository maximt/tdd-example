
from django.test import TestCase
from lists.forms import ItemForm


class ItemFormTest(TestCase):

    def test_form_renders_item_text(self):
        form = ItemForm()
        self.fail(form.as_p())

    def test_form_item_input_has_placeholder_and_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())