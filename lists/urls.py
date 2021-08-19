from django.urls import path
from lists import views


urlpatterns = [
    path('<list_id>/', views.page_list, name='page_list'),
    path('new', views.new_list, name='new_list'),
    path('users/<email>/', views.my_lists, name='my_lists'),
]
