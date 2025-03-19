from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.signals import request_finished
from kasa.models import Order

# Create a notifications model. 

class Notifications(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_user")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_author")
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    date_modified = models.DateTimeField(User, auto_now_add=True)

    class Meta:
        ordering = ['-date_modified']
        verbose_name_plural = "Zawiadomienia"

    def __str__(self):
        return f'Zawiadomienie - {str(self.id)}'        

# Signal Receivers (post_save) for Order. If Order created, the receivers will save new Notification object with User and Author. 

@receiver(post_save, sender=Order)
def sent_notification(sender, instance, created, **kwargs):
    if instance.order_user:
        if created:
            user = instance.order_user
            author = instance.order_company
            message = f'{user}, Twoje zamówienie zostało złożone u {author}, poinformujemy Ciebie jak zostanie wysłane!'
            notification = Notifications(user=user, author=author, message=message)
            notification.save()

    if instance.order_shipped:
        user = instance.order_user
        author = instance.order_company
        message = f'Witaj {user}, Twoje zamówienie zostało wysłane.'
        notification = Notifications(user=user, author=author, message=message)
        notification.save()