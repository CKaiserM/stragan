# Generated by Django 5.1.4 on 2025-03-14 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprzedawca', '0007_alter_companyprofile_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='company_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
