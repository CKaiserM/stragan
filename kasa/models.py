from django.db import models
from django.contrib.auth.models import User
from rynek.models import Address, Product
from django.db.models.signals import post_save

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
    
# Create shipping address
def create_shipping_address(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()
post_save.connect(create_shipping_address, sender=User)
    
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

class Order(models.Model):
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_full_name = models.CharField(max_length=255)
    order_email = models.CharField(max_length=255, blank=True, null=True, default='')
    order_shipping_address = models.TextField(max_length=255254, default='')
    order_amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    order_date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Zamówienie - {str(self.id)}'

class OrderItems(models.Model):
    items_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    items_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    items_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    items_quantity = models.PositiveBigIntegerField(default=1)
    items_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'Przedmiot zamówienia - {str(self.id)}'