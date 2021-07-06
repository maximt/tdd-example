from django.urls import path
from lists import views


urlpatterns = [
    path('<list_id>/', views.page_list, name='page_list'),
    path('<list_id>/add_item', views.add_item, name='add_item'),
    path('new', views.new_list, name='new_list'),
]
