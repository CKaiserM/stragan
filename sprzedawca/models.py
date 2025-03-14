from django.db import models
from django.contrib.auth.models import User
from rynek.models import Profile

class CompanyProfile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    company_name = models.CharField(max_length=120, null=True, blank=True)
    company_logo = models.ImageField(null=True, blank=True)
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