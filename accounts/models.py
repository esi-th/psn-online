from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_picture = models.ImageField('Profile Picture', upload_to='profile_pictures/', blank=True, null=True)
    about_me = models.CharField('About Me', max_length=600, blank=True)


class Wishlist(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='Wishlist')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='User', related_name='wishlist')
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Wishlist User: {self.user} Product: {self.product}'
