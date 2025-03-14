from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views


urlpatterns = [
    path('kokpit', views.SellerDashboardView.as_view(), name="dashboard"),
    path('konto-sprzedawcy', views.CompanyProfileView.as_view(), name="copmany_profile"),
    path('aktualizuj-konto', views.CompanyProfileView.update_company_profile, name="update_company_profile"),
    path('dodaj-konto', views.CompanyProfileView.create_company_profile, name="create_company_profile"),
    path('usun-konto', views.CompanyProfileView.delete_company_profile, name="delete_company_profile")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

