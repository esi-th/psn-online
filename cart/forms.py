from django import forms
from products.models import Guarantee


class AddProductToCartForm(forms.Form):
    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 31)]
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)
    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)
    guarantee = forms.CharField(max_length=2)
