# Generated by Django 5.1.4 on 2025-03-07 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kasa', '0009_shippingmethod_shipping_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShippingMethod',
        ),
    ]
