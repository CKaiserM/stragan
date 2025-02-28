from . import models

def navbar(request):
    nav_products = models.Product.objects.all()
    nav_featured_products = models.FeaturedProducts.objects.all()
    nav_categories = models.Category.objects.all()
    nav_subcategories = models.Subcategory.objects.all()
    return {'nav_products':nav_products, 'nav_featured_products':nav_featured_products, 'nav_categories':nav_categories, 'nav_subcategories':nav_subcategories}

