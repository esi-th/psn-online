from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from ckeditor.fields import RichTextField


class Guarantee(models.Model):
    NO_GUARANTEE = 'ng'
    ONE_YEAR_GUARANTEE = '1y'
    TWO_YEAR_GUARANTEE = '2y'
    THREE_YEAR_GUARANTEE = '3y'
    GUARANTEE_CHOICES = [
        (NO_GUARANTEE, 'No Guarantee'),
        (ONE_YEAR_GUARANTEE, '1 Years Guarantee'),
        (TWO_YEAR_GUARANTEE, '2 Years Guarantee'),
        (THREE_YEAR_GUARANTEE, '3 Years Guarantee'),
    ]
    name = models.CharField('Name', max_length=2, choices=GUARANTEE_CHOICES, default=NO_GUARANTEE)
    price = models.IntegerField('Price')
    description = models.CharField('Description', max_length=500)
    datetime_created = models.DateTimeField('Created On', auto_now_add=True)

    def __str__(self):
        return f'{self.name}: {self.price}'


class Category(models.Model):
    name = models.CharField('Name', max_length=255)
    description = models.CharField('Description', max_length=500, blank=True)
    # top_product = models.ForeignKey('Product', on_delete=models.SET_NULL,
    #                                 null=True, related_name='+', verbose_name='Top Product')
    datetime_created = models.DateTimeField('Created On', auto_now_add=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    discount = models.FloatField('Discount')
    code = models.CharField('Code', max_length=255)
    used = models.BooleanField('Used', default=False)


class Tag(models.Model):
    name = models.CharField('Tag Name', max_length=255)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField('Color', max_length=255)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField('Company', max_length=255)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField('Model', max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField('Title', max_length=255)
    description = RichTextField()
    features = models.JSONField()
    price = models.PositiveIntegerField('Price')
    cover = models.ImageField('Cover', upload_to='product_covers/', blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Company')
    model = models.ForeignKey(ProductModel, on_delete=models.PROTECT, verbose_name='Model')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category')
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True)
    inventory = models.PositiveIntegerField('Inventory')
    active = models.BooleanField('Show In List', default=True)
    colors = models.ManyToManyField(Color, verbose_name='Colors', blank=True)
    discounts = models.ManyToManyField(Discount, blank=True, verbose_name='Discounts')
    slug = models.SlugField()
    datetime_created = models.DateTimeField('Created On', auto_now_add=True)
    datetime_modified = models.DateTimeField('Modified On', auto_now=True)

    def __str__(self):
        return f'{self.id}: {self.title}'

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name='Product')
    image = models.ImageField('Image', upload_to='product_images/')


class Review(models.Model):
    PRODUCT_STARS_CHOICES = [
        ('1', 'Very Bad'),
        ('2', 'Bad'),
        ('3', 'Normal'),
        ('4', 'Good'),
        ('5', 'Perfect'),
    ]
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Author')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='reviews')
    body = models.CharField('Review Text', max_length=700)
    stars = models.CharField('Stars', max_length=1, choices=PRODUCT_STARS_CHOICES)
    active = models.BooleanField('Show', default=False)
    recommend = models.BooleanField('Recommend', default=True)
    datetime_created = models.DateTimeField('Created On', auto_now_add=True)
    datetime_modified = models.DateTimeField('Modified On', auto_now=True)

    def __str__(self):
        return f"Review by {self.author} for {self.product}"

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.product.id])


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS_CHOICES = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]
    body = models.CharField('Comment Text', max_length=1000)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               verbose_name='Author', related_name='product_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Product', related_name='product_comments')
    status = models.CharField('Status', max_length=2, choices=COMMENT_STATUS_CHOICES, default=COMMENT_STATUS_WAITING)
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    datetime_modified = models.DateTimeField('Modified On', auto_now=True)
    datetime_created = models.DateTimeField('Created On', auto_now_add=True)

    def __str__(self):
        return f'ID: {self.id} | Post: {self.product} | Author: {self.author}'

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.product.id])
