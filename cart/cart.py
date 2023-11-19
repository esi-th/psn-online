from django.contrib import messages
from products.models import Product, Guarantee


class Cart:
    def __init__(self, request):
        """
        initialize cart
        """
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1, replace_quantity=False, guarantee_name=None):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        if guarantee_name == 'ng':
            self.cart[product_id]['product_guarantee'] = 'No Guarantee'
            self.cart[product_id]['guarantee_price'] = 0
            self.cart[product_id]['guarantee_description'] = ''
        else:
            guarantee = Guarantee.objects.filter(name=guarantee_name).first()
            if guarantee:
                self.cart[product_id]['product_guarantee'] = guarantee_name
                self.cart[product_id]['guarantee_price'] = guarantee.price
                self.cart[product_id]['guarantee_description'] = guarantee.description

        if replace_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        messages.success(self.request, "Product Successfully Added To Cart.")

        self.save()

    def save(self):
        """
        mark session as modified to save changes
        """
        self.session.modified = True

    def remove(self, product):
        """
        remove specified product from the cart
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, "Product Successfully Removed From Cart.")
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = (item['product_obj'].price * item['quantity']) + \
                                  (item['guarantee_price'] * item['quantity'])
            yield item

    def clear(self):
        """
        clear the cart from every product
        """
        del self.session['cart']
        self.save()

    def __len__(self):
        """
        returns length of items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        iterate on products in cart and return sum of items prices
        """
        return sum((item['quantity'] * item['product_obj'].price) +
                   (item['quantity'] * item['guarantee_price']) for item in self.cart.values())

    def is_empty(self):
        if self.cart:
            return False
        return True
