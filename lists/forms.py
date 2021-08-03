from django import forms
from lists.models import Item


MSG_EMPTY_ITEM_ERROR = "You can't have empty list item"


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter item',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {'required': MSG_EMPTY_ITEM_ERROR}
        }
