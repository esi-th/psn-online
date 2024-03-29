# Generated by Django 4.2.7 on 2023-11-17 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Category Name')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('status', models.CharField(choices=[('p', 'Published'), ('d', 'Draft')], default='d', max_length=2, verbose_name='Status')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('likes', models.PositiveIntegerField(verbose_name='Likes')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='Created On')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Modified On')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.category', verbose_name='Category')),
                ('tags', models.ManyToManyField(to='blog.tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=1000, verbose_name='Comment Text')),
                ('status', models.CharField(choices=[('w', 'Waiting'), ('a', 'Approved'), ('na', 'Not Approved')], default='w', max_length=2)),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='Created On')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Modified On')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='Post')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.comment')),
            ],
        ),
    ]
