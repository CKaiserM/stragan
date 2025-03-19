from . import models
from eka.models import Notifications

def navbar(request):
    nav_products = models.Product.objects.all()
    nav_featured_products = models.FeaturedProducts.objects.all()
    nav_categories = models.Category.objects.all()
    nav_subcategories = models.Subcategory.objects.all()
    if request.user.is_authenticated:
        unread_notifications = Notifications.objects.filter(user=request.user, read=False).count()
        return {'nav_products':nav_products, 'nav_featured_products':nav_featured_products, 'nav_categories':nav_categories, 'nav_subcategories':nav_subcategories, 'unread_notifications':unread_notifications}
    else:
        return {'nav_products':nav_products, 'nav_featured_products':nav_featured_products, 'nav_categories':nav_categories, 'nav_subcategories':nav_subcategories}

