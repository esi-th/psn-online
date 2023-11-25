from django.contrib import admin
from .models import ContactUs, TopSlider, DiscountSlider, TopProduct


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['message_name', 'message_email', 'message_note', ]


admin.site.register(TopSlider)
admin.site.register(DiscountSlider)
admin.site.register(TopProduct)

