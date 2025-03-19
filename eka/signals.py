from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Notifications
from kasa.models import Order

@receiver(post_save, sender=Order)
def sent_status_notification(sender, instance, created, **kwargs):
    if instance.order_shipped:
        print("in")
        user = instance.order_user
        author = instance.order_company
        message = f'Witaj {user}, Twoje zamówienie zostało wysłane.'
        notification = Notifications(user=user, author=author, message=message)
        notification.save()