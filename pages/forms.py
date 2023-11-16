from django import forms
from .models import ContactUs


class ContactUsFrom(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['message_name', 'message_email', 'message_note']
