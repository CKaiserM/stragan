from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

import after_response
import json

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from koszyk.cart import Cart
from rynek.models import Product
from kasa.forms import ShippingAddressForm
from kasa.models import ShippingAddress

class PaymentSuccessView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'kasa/payment_success.html'

    def get(self, request):
        
        return Response({})
    
class CheckoutView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'kasa/checkout.html'

    def get(self, request):
        cart = Cart(request)
        cart_checkout = cart.get_products
        cart_quantities = cart.get_quantity
        cart_total = cart.get_cart_total
        cart_subtotal = cart.get_cart_subtotal
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        if request.user.is_authenticated:
            shipping_address_form = ShippingAddressForm(request.POST or None, instance=shipping_user)
            return Response({'cart_checkout':cart_checkout, 'cart_quantities':cart_quantities, 'cart_total':cart_total, 'cart_subtotal':cart_subtotal, 'shipping_address_form':shipping_address_form, 'shipping_user':shipping_user})
        else:
            shipping_address_form = ShippingAddressForm(request.POST or None)
            return Response({'cart_checkout':cart_checkout, 'cart_quantities':cart_quantities, 'cart_total':cart_total, 'cart_subtotal':cart_subtotal, 'shipping_address_form':shipping_address_form})