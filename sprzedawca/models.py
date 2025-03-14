from django.db import models
from django.contrib.auth.models import User
from rynek.models import Profile

from django.db.models.signals import post_save

class CompanyProfile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    company_name = models.CharField(max_length=120, null=True, blank=True)
    company_email = models.EmailField(max_length=254, null=True, blank=True, unique=True)
    company_logo = models.ImageField(blank=True, upload_to="images/company_profile/")
    nip = models.CharField(max_length=20, null=True, blank=True)
    regon = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True, default="brak numeru")
    house_and_street_no = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=120, default='')
    postal_code = models.CharField(max_length=6, default='')
    country = models.CharField(max_length=255, default='Polska')
    #payment_methods = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return f'{self.company_name} - {self.user}'
    
    class Meta:
        verbose_name_plural = "Profile Firmowe"
