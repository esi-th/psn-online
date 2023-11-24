from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from orders.models import Order


def account_page_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    return render(request, 'accounts/account_hub.html')


@login_required
def dashboard_page_view(request):
    return render(request, 'accounts/dashboard.html')


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user == request.user:
        return render(request, 'accounts/order_detail.html', context={
            'order': order,
        })

    return redirect(reverse('home'))
