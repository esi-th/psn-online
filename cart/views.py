from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddProductToCartForm
from .cart import Cart
from products.models import Product


def cart_detail_view(request):
    cart = Cart(request)

    for item in cart:
        item['product_update_quantity_form'] = AddProductToCartForm(initial={
            'quantity': item['quantity'],
            'guarantee': item['guarantee_name'],
            'inplace': True,
        })

    return render(request, 'cart/cart_detail.html', context={
        'cart': cart,
    })


def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    form = AddProductToCartForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        print(quantity, product, cleaned_data['guarantee'], cleaned_data['inplace'])
        cart.add(product, quantity, replace_quantity=cleaned_data['inplace'], guarantee_name=cleaned_data['guarantee'])

    return redirect('cart:cart_detail')


def remove_from_cart_view(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')


def clear_cart_view(request):
    cart = Cart(request)

    if cart:
        cart.clear()

    return redirect('cart:cart_detail')
