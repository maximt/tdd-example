from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Item, List


def home_page(request):
    return render(request, 'home.html')

def page_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(f'/lists/{list_.id}/')
        except ValidationError:
            error = "You can't have empty list item"
        
    return render(request, 'list.html', context={'list': list_, 'error': error})

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST.get('item_text', ''), list=list_)

    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have empty list item"
        return render(request, 'home.html', context={'error': error})

    return redirect(f'/lists/{list_.id}/')
