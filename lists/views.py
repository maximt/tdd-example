from django.shortcuts import render, redirect
from .models import Item, List


def home_page(request):
    return render(request, 'home.html')

def page_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', context={'items': items})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get('item_text', ''), list=list_)
    return redirect('/lists/my-single-list/')