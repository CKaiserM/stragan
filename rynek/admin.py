from django.contrib import admin
from .models import Product, Category

# Register products
admin.site.register(Product)
admin.site.register(Category)