# Generated by Django 5.1.4 on 2025-03-14 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprzedawca', '0006_alter_companyprofile_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='company_logo',
            field=models.ImageField(blank=True, upload_to='images/company_profile/'),
        ),
    ]
