from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
#from django.utils.text import slugify
import datetime
from slugify import slugify

from PIL import Image, ImageOps


# Prduct categories
class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Kategorie"

# Prduct categories
class Subcategory(models.Model):
    name = models.CharField(max_length=120)
    parent_name = models.ForeignKey(Category, related_name='sub_categories', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'- {self.parent_name} - {self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.parent_name.name + ' ' + self.name)

        super(Subcategory, self).save(*args, **kwargs)
        #featured image resize
        output_size = (400, 300)
        with Image.open(self.image.path) as im:
            ImageOps.cover(im, output_size).save(self.image.path)
            im.thumbnail(output_size)
            im.save(self.image.path)
    
    class Meta:
        verbose_name_plural = "Podkategorie"

class Address(models.Model):
    street = models.CharField(max_length=255, default='')
    house_number = models.CharField(max_length=5, default='')
    flat_number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=120, default='')
    postal_code = models.CharField(max_length=6, default='')
    province = models.CharField(max_length=32, default='')
    voivodeship = models.CharField(max_length=32, default='')

    def __str__(self):
        return f'{self.city} {self.street} {self.house_number}'
    
    class Meta:
        verbose_name_plural = "Adres użytkownika"

# Profile profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    first_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    is_company = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, null=True, blank=True, default="brak numeru")
    house_and_street_no = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=120, default='')
    postal_code = models.CharField(max_length=6, default='')
    country = models.CharField(max_length=255, default='Polska')
    old_cart = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name_plural = "Profile użytkowników"



# Create a seller profile
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
post_save.connect(create_profile, sender=User)

class Customer(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    password = models.CharField(max_length=120)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name_plural = "Klienci"   

class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    unit = models.CharField(max_length=120, default="Kilogram")
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, default=1)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(upload_to='uploads/product/')
    images = models.ImageField(upload_to='uploads/product/')
    status = models.BooleanField(default=True)

    is_on_sale = models.BooleanField(default=False)
    price_on_sale = models.DecimalField(default=0, decimal_places=2, max_digits=12)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super(Product, self).save(*args, **kwargs)
        #featured image resize
        output_size = (400, 300)
        with Image.open(self.featured_image.path) as im:
            ImageOps.cover(im, output_size).save(self.featured_image.path)
            im.thumbnail(output_size)
            im.save(self.featured_image.path)
        
        #featured image resize
        lg_output_size = (800, 600)
        with Image.open(self.images.path) as img:
            ImageOps.cover(img, lg_output_size).save(self.images.path)
            img.thumbnail(lg_output_size)
            img.save(self.images.path)

    class Meta:
        verbose_name_plural = "Produkty"          

class FeaturedProducts(models.Model):
    featured = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.featured.title
    
    class Meta:
        verbose_name_plural = "Sponsorowane produkty"

