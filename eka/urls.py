from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.NotificationsView.as_view(), name="notifications"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)