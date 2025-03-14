from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('kokpit', views.SellerDashboardView.as_view(), name="dashboard"),
    path('konto-sprzedawcy', views.CompanyProfileView.as_view(), name="copmany_profile"),
]

