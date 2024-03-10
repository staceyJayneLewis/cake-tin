from django.urls import path
from . import views

urlpatterns = [
    path('', views.basket, name='basket'),
    path('add/<item>/', views.add_to_basket, name='add_to_basket'),
    path('amend/<item>/', views.amend_basket, name='amend_basket'),
    path('remove/<item>/', views.remove_basket, name='remove_basket'),
]
