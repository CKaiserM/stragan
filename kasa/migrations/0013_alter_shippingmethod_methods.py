# Generated by Django 5.1.4 on 2025-03-08 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kasa', '0012_shippingmethod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingmethod',
            name='methods',
            field=models.CharField(choices=[('Odbiór osobisty', [('koszt', '0'), ('czas', '0')]), ('Kurier', [('koszt', '15.99'), ('czas', '1-2')]), ('Poczta', [('koszt', '3.99'), ('czas', '2-4')])], default=2, max_length=25),
        ),
    ]
