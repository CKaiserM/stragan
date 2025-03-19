from .models import Notifications

from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import redirect

import after_response

# Following function enables action after Notification is opened (sets read attribute too: true). 

@after_response.enable
def notifications_read(request):
    notifications = Notifications.objects.filter(user=request.user)
    for object in notifications:
        object.read = True
        object.save()

# Notifications view class

class NotificationsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    model = Notifications
    template_name = 'notifications.html'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            notifications = Notifications.objects.filter(user=request.user).order_by('-date_modified')
            unread_notifications = Notifications.objects.filter(user=request.user, read=False).count()
            notifications_read.after_response(request)
            return Response({'notifications': notifications, 'unread_notifications':unread_notifications})
        else:
            return redirect('login')