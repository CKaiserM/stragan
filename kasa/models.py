from django.db import models
from django.contrib.auth.models import User
from rynek.models import Product
from django.db.models.signals import post_save, pre_save
import datetime
from django.dispatch import receiver

class ShippingMethod(models.Model):
    METHODS = (
        (1, "Odbiór osobisty"),
        (2, "Kurier"),
        (3, "Poczta"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    methods = models.IntegerField(choices=METHODS, default=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.CharField(max_length=25, default='1-2')

    class Meta:
        verbose_name_plural = "Metody dostawy"

    def __str__(self):
        return f'Dostawa - {self.methods}'

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255, blank=True, null=True)
    shipping_house_and_street_no = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=120)
    shipping_postal_code = models.CharField(max_length=6)
    shipping_country = models.CharField(max_length=255, default='Polska')

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
    
class PaymentMethods(models.Model):
    payment_name = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = "Metody płatności"

    def __str__(self):
        return self.payment_name

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

    class Meta:
        verbose_name_plural = "Dane do faktury"

class Order(models.Model):
    order_company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_seller", null=True, blank=True)
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="order_buyer")
    order_full_name = models.CharField(max_length=255)
    order_email = models.CharField(max_length=255, blank=True, null=True, default='')
    order_shipping_address = models.TextField(max_length=255254, default='')
    order_amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    order_date_ordered = models.DateTimeField(auto_now_add=True)
    order_shipping_method = models.CharField(max_length=255)
    order_shipped = models.BooleanField(default=False)
    order_date_shipped = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Zamówienie"

    def __str__(self):
        return f'Zamówienie - {str(self.id)}'
    
# Save the shipping date automaticly
@receiver(pre_save, sender=Order)
def date_shipped(sender, instance, **kwargs):
    if instance.pk:
        date_now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        # Save time and date if order_shipped is true
        if instance.order_shipped and not obj.order_shipped:
            instance.order_date_shipped = date_now

class OrderItems(models.Model):
    items_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    items_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    items_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="item_buyer")
    items_company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item_seller", null=True, blank=True)

    items_quantity = models.PositiveBigIntegerField(default=1)
    items_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name_plural = "Szczegóły zamówienia"

    def __str__(self):
        return f'Przedmiot zamówienia - {str(self.id)}'
    
