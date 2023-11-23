from django.shortcuts import render, redirect, reverse
from django.views import generic

from orders.models import Order


def account_page_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    return render(request, 'accounts/account_hub.html')

