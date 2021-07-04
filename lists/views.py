from django.shortcuts import render, redirect
from .models import Item


def home_page(request):
    return render(request, 'home.html')

def page_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', context={'items': items})

def new_list(request):
    Item.objects.create(text=request.POST.get('item_text', ''))
    return redirect('/lists/my-single-list/')