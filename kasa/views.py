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

class PaymentSuccessView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'kasa/payment_success.html'

    def get(self, request):
        return Response({})