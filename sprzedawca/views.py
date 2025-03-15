from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from rynek.models import Profile

from .forms import CompanyInfoForm
from .models import CompanyProfile
from kasa.models import Order

class SellerDashboardView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'firma/dashboard.html'

    def get(self, request):
        
        if request.user.is_authenticated:
            orders_not_shipped = Order.objects.filter(order_shipped=False)
            orders_shipped = Order.objects.filter(order_shipped=True)
            
            return Response({"orders_not_shipped":orders_not_shipped, 'orders_shipped':orders_shipped})
        else:
            messages.success(request, ("Niedozwolona akcja"))
            return redirect('home')

    def shipped(request):
        if request.user.is_authenticated:
            if request.method == "POST":
                order_id = request.POST['status']
                order = Order.objects.filter(id=order_id)
                now = datetime.now()
                order.update(order_shipped=False, order_date_shipped=now)
                return redirect(request.META.get("HTTP_REFERER"))

    def not_shipped(request):
        if request.user.is_authenticated:
            if request.method == "POST":
                order_id = request.POST['status']
                order = Order.objects.filter(id=order_id)
                now = datetime.now()
                order.update(order_shipped=True, order_date_shipped=now)
                return redirect(request.META.get("HTTP_REFERER"))

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

