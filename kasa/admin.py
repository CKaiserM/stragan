from django.contrib import admin
from .models import ShippingAddress, Order, OrderItems, ShippingMethod, PaymentMethods
# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(ShippingMethod)
admin.site.register(PaymentMethods)

class OrderItemsInline(admin.StackedInline):
    model = OrderItems
    extra = 0
    

class Orders(admin.ModelAdmin):
    model = Order
    readonly_fields = ["order_date_ordered"]
    fields = ["order_user", "order_full_name", "order_email", "order_shipping_address", "order_amount_paid", "order_date_ordered"]
    inlines = [OrderItemsInline]

admin.site.unregister(Order)
admin.site.register(Order, Orders)

