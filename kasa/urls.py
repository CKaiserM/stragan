from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('payment_success', views.PaymentSuccessView.as_view(), name="payment_success"),
    path('checkout', views.CheckoutView.as_view(), name="checkout"),
    path('shipping', views.CheckoutView.shipping, name="shipping"),
    path('payment', views.CheckoutView.payment, name="payment"),
    path('process_order', views.CheckoutView.process_order, name="process_order"),
]
