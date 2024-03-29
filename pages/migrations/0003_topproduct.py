# Generated by Django 4.2.7 on 2023-11-24 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_guarantee_price'),
        ('pages', '0002_topslider_discountslider'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(upload_to='discount_slider_covers/', verbose_name='Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Product')),
            ],
        ),
    ]
