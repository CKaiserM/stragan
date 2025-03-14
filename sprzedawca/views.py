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

from rynek.models import Product, Profile, FeaturedProducts, Category, Subcategory
from rynek.forms import SignUpForm, UpdateUserForm, UserInfoForm
from kasa.forms import ShippingAddressForm
from kasa.models import ShippingAddress
from koszyk.cart import Cart
from .forms import CompanyInfoForm
from .models import CompanyProfile

class SellerDashboardView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'firma/dashboard.html'

    def get(self, request):
        
        if request.user.is_authenticated:
            company_profile = CompanyProfile.objects.get(user__id=request.user.id)
             
            return Response({"company_profile":company_profile})
        else:
            messages.success(request, ("Niedozwolona akcja"))
            return redirect('home')    
        
class CompanyProfileView(APIView):
    renderer_classes= [TemplateHTMLRenderer]
    template_name = 'firma/company_profile.html'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        company_profile = CompanyProfile.objects.get(user__id=request.user.id)
        company_info = CompanyInfoForm(request.POST or None, request.FILES or None, instance=company_profile)      
        return Response({"company_profile":company_profile, 'company_info':company_info})
    
    def create_company_profile(request):
        current_user = Profile.objects.get(user__id=request.user.id)
        profile_exist = CompanyProfile.objects.filter(user__id=request.user.id).exists()
        if request.user.is_authenticated and not current_user.is_company and not profile_exist:
            if request.method == "POST":
                add_profile = CompanyProfile(user=current_user)
                current_user.is_company = True   
                add_profile.save()    
                current_user.save()
                return redirect('dashboard')
        else:
            return redirect('home')

    def delete_company_profile(request):
        current_user = Profile.objects.get(user__id=request.user.id)
        profile_exist = CompanyProfile.objects.get(user__id=request.user.id)
        if request.user.is_authenticated and current_user.is_company and profile_exist:
            if request.method == "POST":
                current_user.is_company = False
                current_user.save() 
                profile_exist.delete()
                return redirect('home')
        else:
            return redirect('home')

    def update_company_profile(request):
        if request.user.is_authenticated:
            current_user = CompanyProfile.objects.get(user__id=request.user.id)
            company_info = CompanyInfoForm(request.POST or None, request.FILES or None, instance=current_user)
             
            if company_info.is_valid():
                company_info.save()   
        return redirect(request.META.get("HTTP_REFERER"))

