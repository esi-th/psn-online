from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order
from products.models import Product
from .models import Wishlist
from django.http import HttpResponseRedirect


def account_page_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    return render(request, 'accounts/account_hub.html')


@login_required
def dashboard_page_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'accounts/dashboard.html', context={
        'wishlist': wishlist,
    })


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user == request.user:
        return render(request, 'accounts/order_detail.html', context={
            'order': order,
        })

    return redirect(reverse('home'))


@login_required
def add_to_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product:
        if Wishlist.objects.filter(user=request.user, product_id=product_id):
            messages.warning(request, 'Product Already Is In Your Wishlist!')
        else:
            Wishlist.objects.create(user=request.user, product=product)
            messages.success(request, 'Product Has Successfully Added To Your Wishlist.')
    else:
        messages.warning(request, 'No Such Product Found!')
    return HttpResponseRedirect(reverse('products:product_detail', args=[product.id]))


@login_required
def remove_from_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if Wishlist.objects.filter(user=request.user, product_id=product_id):
        wishlist_item = Wishlist.objects.get(product_id=product_id)
        wishlist_item.delete()
        messages.success(request, 'Product Has Successfully Removed From Your Wishlist.')
    else:
        messages.warning(request, 'No Such Product Found In Your Wishlist')

    return HttpResponseRedirect(reverse('products:product_detail', args=[product.id]))
