from django.db import models


class ContactUs(models.Model):
    message_name = models.CharField('Name', max_length=50)
    message_email = models.EmailField('Email', )
    message_note = models.CharField('Note', max_length=600)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Name: {self.message_name} | Email: {self.message_email}'
