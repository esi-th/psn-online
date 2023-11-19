from django.contrib import admin
from . import models


class CommentInlines(admin.TabularInline):
    model = models.Comment
    extra = 1


class ReviewInlines(admin.TabularInline):
    model = models.Review
    extra = 1


@admin.register(models.Guarantee)
class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'datetime_created', ]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'datetime_created', ]


@admin.register(models.Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['discount', 'code', 'used', ]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'company', 'model', 'category', 'inventory', 'datetime_modified', 'active', ]
    inlines = [
        CommentInlines,
        ReviewInlines,
    ]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'product', 'stars', 'recommend', 'datetime_modified', 'active', ]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'product', 'status', 'datetime_modified', ]


admin.site.register(models.Tag)
admin.site.register(models.Color)
admin.site.register(models.Company)
admin.site.register(models.ProductModel)
