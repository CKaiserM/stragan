from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group

from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from rynek.models import Profile

from .forms import CompanyInfoForm, AddProductForm, AddProductImagesForm
from .models import CompanyProfile
from kasa.models import Order
from rynek.models import Product, ProductImages

class SellerDashboardView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'firma/dashboard.html'

    def get(self, request):
        #check if user is in seller group
        in_group = request.user.groups.filter(name="Sprzedawca").exists()
        
        if request.user.is_authenticated and in_group:
            orders_not_shipped = Order.objects.filter(order_shipped=False, order_company=request.user)
            orders_shipped = Order.objects.filter(order_shipped=True, order_company=request.user)
            
            return Response({"orders_not_shipped":orders_not_shipped, 'orders_shipped':orders_shipped})
        else:
            messages.success(request, ("Niedozwolona akcja"))
            return redirect('home')

    def shipped(request):
        #check if user is in seller group
        in_group = request.user.groups.filter(name="Sprzedawca").exists()
        #check if user is in seller group
        if request.user.is_authenticated and in_group:
            if request.method == "POST":
                order_id = request.POST['status']
                order = Order.objects.get(id=order_id)
                now = datetime.now()
                order.order_shipped = False 
                order.order_date_shipped = now
                order.save()
                
                return redirect(request.META.get("HTTP_REFERER"))

    def not_shipped(request):
        #check if user is in seller group
        in_group = request.user.groups.filter(name="Sprzedawca").exists()

        if request.user.is_authenticated and in_group:
            if request.method == "POST":
                order_id = request.POST['status']
                order = Order.objects.get(id=order_id)
                now = datetime.now()
                order.order_shipped = True 
                order.order_date_shipped = now
                order.save()
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
                #add user to Group
                Group.objects.get(name='Sprzedawca').user_set.add(request.user)
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
        #check if user is in seller group
        in_group = request.user.groups.filter(name="Sprzedawca").exists()
        if request.user.is_authenticated and in_group:
            current_user = CompanyProfile.objects.get(user__id=request.user.id)
            company_info = CompanyInfoForm(request.POST or None, request.FILES or None, instance=current_user)
             
            if company_info.is_valid():
                company_info.save()   
        return redirect(request.META.get("HTTP_REFERER"))
    
class ProductManagerView(APIView):
    renderer_classes= [TemplateHTMLRenderer]
    template_name = 'firma/product_manager.html'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        #check if user is in seller group
        in_group = request.user.groups.filter(name="Sprzedawca").exists()
        if request.user.is_authenticated and in_group:
            products = Product.objects.filter(user=request.user)
            form = AddProductForm()
            images = AddProductImagesForm()
            return Response({"products":products, 'form':form, 'images':images})
        else:
            return redirect('home')

class AddProductView(APIView):
    renderer_classes= [TemplateHTMLRenderer]
    template_name = 'firma/add_product.html'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        #check if user is in seller group
        in_group = request.user.groups.filter(name="Sprzedawca").exists()
        if request.user.is_authenticated and in_group:
            products = Product.objects.filter(user__id=request.user.id)
            form = AddProductForm()
            images = AddProductImagesForm()
            
            return Response({"products":products})
        else:
            return redirect('home')
    
    def post(self, request):
        
        #check if user is in seller group
        in_group = request.user.groups.filter(name="Sprzedawca").exists()

        form = AddProductForm()
        images_form = AddProductImagesForm()
        if request.user.is_authenticated and in_group:
            form = AddProductForm(request.POST or None, request.FILES or None)
            images_form = AddProductImagesForm(request.FILES.getlist('image') or None)
            
            #get list of all aimages
            #todo: max images added
            images = request.FILES.getlist('image')

            if form.is_valid(): 
                product = form.save(commit=False)
                # Set user for newly created product
                product.user = request.user
                product.save()
                for img in images:
                    ProductImages(product=product, images=img).save()
        return redirect(request.META.get("HTTP_REFERER"))

class UpdateProductView(APIView):
    renderer_classes= [TemplateHTMLRenderer]
    template_name = 'firma/update_product.html'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        #check if user is in seller group
        in_group = request.user.groups.filter(name="Sprzedawca").exists()
        if request.user.is_authenticated and in_group:
            product = get_object_or_404(Product, id=pk)
            image = ProductImages.objects.filter(product=pk)
            form = AddProductForm(instance=product)
            images = AddProductImagesForm(instance=product)
            
            return Response({"product":product, 'form':form, 'images':images})
        else:
            return redirect('home')
    
    def post(self, request, pk):
        
        #check if user is in seller group
        in_group = request.user.groups.filter(name="Sprzedawca").exists()
        product = get_object_or_404(Product, id=pk)
        form = AddProductForm()
        images_form = AddProductImagesForm()
        if request.user.is_authenticated and in_group:
            form = AddProductForm(request.POST or None, request.FILES or None, instance=product)
            images_form = AddProductImagesForm(request.FILES.getlist('image') or None, instance=product)

            if form.is_valid(): 
                product = form.save(commit=False)
                # Set user for newly created product
                product.user = request.user
                product.save()
                #get list of all aimages
                #todo: max images added
                if request.FILES.getlist('image'):
                    images = request.FILES.getlist('image')

                    for img in images:
                        ProductImages(product=product, images=img).save()
        return redirect('copmany_products')

