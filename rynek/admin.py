from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Product, Category, Subcategory, Profile, Address, FeaturedProducts, Customer


# Register products
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Address)
admin.site.register(FeaturedProducts)


# Combine profile info and user
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend user model

class UserAdmin(admin.ModelAdmin):
    model = User
    #display only username
    fields = ["username", "email"]
    inlines = [ProfileInline]

# Unregister initial User
admin.site.unregister(User)

# Register user and profile
admin.site.register(User, UserAdmin)
admin.site.register(Profile)

