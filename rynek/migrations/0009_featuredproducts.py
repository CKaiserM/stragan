# Generated by Django 5.1.4 on 2025-02-27 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rynek', '0008_remove_profile_email_remove_profile_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('featured', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rynek.product')),
            ],
        ),
    ]
