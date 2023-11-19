from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import OrderItem
from .forms import CreateOrderForm
from cart.cart import Cart


def order_create_view(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, "Your Cart Is Empty! You Have To Add Some Products To Your Cart First.")
        return redirect('products:products_list')

    if request.method == 'POST':
        order_form = CreateOrderForm(request.POST)

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            cart_total_price = 0
            order_obj.save()

            for item in cart:
                cart_total_price += (item['quantity'] * item['product_obj'].price) + \
                                  (item['guarantee_price'] * item['quantity'])
                product = item['product_obj']
                OrderItem.objects.create(
                    order=order_obj,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price,
                    guarantee=item['product_guarantee'],
                )
            order_obj.price = cart_total_price
            order_obj.save()

            cart.clear()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()

            request.session['order_id'] = order_obj.id

            messages.success(request, 'Your Order Placed Successfully!')
            return redirect('home')

            # redirect to payment gateway
            # return redirect('payment:payment_process')

    form = CreateOrderForm()
    return render(request, 'orders/order_create.html', context={
        'order_create_form': form,
    })
