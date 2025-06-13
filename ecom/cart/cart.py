from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, qty=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'qty': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['qty'] = qty
        else:
            self.cart[product_id]['qty'] += qty

        self.save()



    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_products(self):
        product_ids = self.cart.keys()
        return Product.objects.filter(id__in=product_ids)

    def get_product_quantity(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            return self.cart[product_id]['qty']
        return 0

    def reduce(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['qty'] > 1:
                self.cart[product_id]['qty'] -= 1
            else:
                self.remove(product)
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session['session_key'] = self.cart
        self.session.modified = True
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            item = self.cart[str(product.id)]
            item["product"] = product  # Attach product object
            item["product_id"] = product.id  # Ensure product_id is accessible
            yield item
    def get_total_price(self):
        total = 0
        for product_id, item in self.cart.items():
            product = Product.objects.get(id=product_id)
            total += product.price * item['qty']
        return total
