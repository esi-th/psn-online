from django import forms
from .models import Order


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'city', 'address', 'note', ]
