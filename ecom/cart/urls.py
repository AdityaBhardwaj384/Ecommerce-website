from django.urls import path
from . import views

urlpatterns= [

    path('',views.cart_summary, name="cart_summary"),
    path('add/',views.cart_add, name="cart_add"),
    path('delete/',views.cart_delete, name="cart_delete"),
    path('update/',views.cart_update, name="cart_update"),
    path('increase/', views.cart_increase, name='cart_increase'),
    path('decrease/', views.cart_decrease, name='cart_decrease'),
    path('remove/', views.cart_remove, name='cart_remove'),
]