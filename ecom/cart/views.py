from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST

def cart_summary(request):
    cart = Cart(request)
    cart_products = list(cart)

    total_price = 0
    for item in cart_products:
        product = item['product']
        qty = item['qty']
        total_price += product.price * qty

    return render(request, 'cart/cart_summary.html', {
        "cart_products": cart_products,
        "total_price": total_price
    })

def cart_add(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        
        current_qty = cart.get_product_quantity(product.id)
        
        # Check stock availability
        if current_qty >= product.quantity:  # Assuming 'stock' is a field in Product model
            return JsonResponse({'error': 'product out of stock!'}, status=400)
        cart.add(product=product)

        response = JsonResponse({'cart_total_qty': cart.__len__(),"cart_total_price": cart.get_total_price()})
        return response

    return HttpResponse(status=400)



def cart_delete(request):
    pass

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def cart_update(request):
    cart = Cart(request)

    try:
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid product ID")

    # If action is 'decrease'
    if request.POST.get('action') == 'decrease':
        cart.reduce(product)
        return JsonResponse({'cart_total_qty': cart.__len__()})

    # Else, update to new quantity (from green Add button)
    quantity = request.POST.get('quantity')
    if quantity is not None:
        try:
            quantity = int(quantity)
        except ValueError:
            return HttpResponseBadRequest("Invalid quantity")

        if quantity <= 0:
            cart.remove(product)
        else:
            cart.add(product, qty=quantity, override_quantity=True)

        return JsonResponse({'qty': cart.__len__()})

    return HttpResponseBadRequest("Invalid request")

@require_POST
def cart_increase(request):
    cart = Cart(request)
    product_id = int(request.POST.get('product_id'))
    product = Product.objects.get(id=product_id)

    current_qty = cart.get_product_quantity(product_id)
    if current_qty >= product.quantity:
        return JsonResponse({'error': 'Cannot add more than available stock'}, status=400)

    cart.add(product)
    return JsonResponse({'qty': cart.get_product_quantity(product_id), 'cart_total_qty': len(cart),"cart_total_price": cart.get_total_price()})

@require_POST
def cart_decrease(request):
    cart = Cart(request)
    product_id = int(request.POST.get('product_id'))
    product = Product.objects.get(id=product_id)

    cart.reduce(product)
    return JsonResponse({'qty': cart.get_product_quantity(product_id), 'cart_total_qty': len(cart),"cart_total_price": cart.get_total_price()})

@require_POST
def cart_remove(request):
    cart = Cart(request)
    product_id = int(request.POST.get('product_id'))
    product = Product.objects.get(id=product_id)

    cart.remove(product)
    return JsonResponse({'qty': 0, 'cart_total_qty': len(cart),"cart_total_price": cart.get_total_price()})
