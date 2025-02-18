from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.KoszykView.summary, name="cart_summary"),
    path('add/', views.KoszykView.add, name="cart_add"),
    path('delete/', views.KoszykView.delete, name="cart_delete"),
    path('update/', views.KoszykView.update, name="cart_update"),
]
