from .models import Category
from cart.cart import Cart

def categories_processor(request):
    return {'categories': Category.objects.all()}

def cart(request):
    return {'cart':Cart(request)}