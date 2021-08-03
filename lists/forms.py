from django import forms


class ItemForm(forms.Form):
    item_text = forms.CharField(
        widget=forms.fields.TextInput(attrs={
            'placeholder': 'Enter item',
            'class': 'form-control input-lg',
        })
    )
