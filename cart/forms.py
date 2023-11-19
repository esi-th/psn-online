from django import forms
from products.models import Guarantee


class AddProductToCartForm(forms.ModelForm):
    class Meta:
        model = Guarantee
        fields = ['name', ]

    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 31)]
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)
    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)
