from django.db import models
import datetime


# Prduct categories
class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Address(models.Model):
    street = models.CharField(max_length=255, default='')
    house_number = models.CharField(max_length=5, default='')
    flat_number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=120, default='')
    postal_code = models.CharField(max_length=6, default='')
    province = models.CharField(max_length=32, default='')
    voivodeship = models.CharField(max_length=32, default='')



# Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    password = models.CharField(max_length=120)
    company = models.CharField(max_length=120, null=True, blank=True)
    nip = models.CharField(max_length=20, null=True, blank=True)
    regon = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    address_differs = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Product(models.Model):
    title = models.CharField(max_length=120)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(upload_to='uploads/product/')
    images = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return self.title


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, default='')
    quantity = models.IntegerField(default=1)
    
    phone = models.CharField(max_length=20)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product