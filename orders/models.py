from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model


class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_PAID,'Paid'),
        (ORDER_STATUS_UNPAID,'Unpaid'),
        (ORDER_STATUS_CANCELED,'Canceled'),
    ]
    CITY_TEHRAN = 'teh'
    CITY_SHIRAZ = 'shz'
    CITY_ESFAHAN = 'esf'
    CITY_CHOICES = [
        (CITY_TEHRAN, 'Tehran'),
        (CITY_SHIRAZ, 'Shiraz'),
        (CITY_ESFAHAN, 'Esfahan'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='User', related_name='orders')
    is_paid = models.BooleanField('Is Paid?', default=False)
    price = models.PositiveIntegerField('Order Total Price', default=0)
    order_status = models.CharField('Order Status', max_length=10,
                                    choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_UNPAID)

    first_name = models.CharField('First Name', max_length=255)
    last_name = models.CharField('Last Name', max_length=255)
    phone_number = PhoneNumberField(verbose_name='Phone Number')
    city = models.CharField('City', max_length=3, choices=CITY_CHOICES, default=CITY_TEHRAN)
    address = models.CharField('Address', max_length=400)
    note = models.CharField('Order Notes', max_length=300, blank=True)

    zarinpal_authority = models.CharField('Zarinpal Authority', max_length=255, blank=True)
    zarinpal_ref_id = models.CharField('Zarinpal Ref ID', max_length=255, blank=True)
    zarinpal_text = models.TextField('Zarinpal Response Data', max_length=700, blank=True)

    datetime_created = models.DateTimeField('Created On',auto_now_add=True)
    datetime_modified = models.DateTimeField('Modified On', auto_now_add=True)

    def __str__(self):
        return f'Order: {self.id} | {self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Order', related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT,
                                verbose_name='Product', related_name='order_items')
    quantity = models.PositiveIntegerField('Quantity', default=1)
    price = models.PositiveIntegerField('Price')
    guarantee = models.CharField('Guarantee', max_length=2)

