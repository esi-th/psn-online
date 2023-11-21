from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_picture = models.ImageField('Profile Picture', upload_to='profile_pictures/', blank=True, null=True)
    about_me = models.CharField('About Me', max_length=600, blank=True)

