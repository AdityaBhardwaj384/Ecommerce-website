from django.contrib import admin
from .models import Category, Customer, Product, Order
from django.contrib.admin.models import LogEntry

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)



