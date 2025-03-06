from django.db import models
from django.contrib.auth.models import User
from rynek.models import Address

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    #address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255, blank=True, null=True, default='')
    shipping_house_and_street_no = models.CharField(max_length=255, default='')
    shipping_city = models.CharField(max_length=120, default='')
    shipping_postal_code = models.CharField(max_length=6, default='')


    class Meta:
        verbose_name_plural = "Adres wysyłki"

    def __str__(self):
        return f'Adres wysyłki - {str(self.id)}'
    
class InvoiceDetails(models.Model):
    company_name = models.CharField(max_length=120, null=True, blank=True)
    company_nip = models.CharField(max_length=20, null=True, blank=True)
    company_street = models.CharField(max_length=255, null=True, blank=True)
    company_house_number = models.CharField(max_length=5, null=True, blank=True)
    company_flat_number = models.IntegerField(null=True, blank=True)
    company_city = models.CharField(max_length=120, null=True, blank=True)
    company_postal_code = models.CharField(max_length=6, null=True, blank=True)
    company_province = models.CharField(max_length=32, null=True, blank=True)
    company_voivodeship = models.CharField(max_length=32, null=True, blank=True)
