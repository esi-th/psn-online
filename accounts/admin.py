from django.contrib import admin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', 'about_me']
    add_fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'about_me', )}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'about_me', )}),
    )




