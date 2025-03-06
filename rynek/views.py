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

from .models import Product, Profile, FeaturedProducts, Category, Subcategory
from .forms import SignUpForm, UpdateUserForm, UserInfoForm
from kasa.forms import ShippingAddressForm
from kasa.models import ShippingAddress
from koszyk.cart import Cart

#Navbar rendering (dynamic links) is included in context_processors.py, and put up in settings.py under TEMPLATES.

#Homepage view
class StraganView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'
    
    def get(self, request):
        products = Product.objects.all()
        featured = FeaturedProducts.objects.all()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        return Response({'products':products, 'featured_products':featured, 'categories':categories, 'subcategories':subcategories})


#Profile view
class ProfileView(APIView):
    renderer_classes= [TemplateHTMLRenderer]
    template_name = 'profile/profile.html'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        profile = Profile.objects.get(user_id=pk)          
        return Response({"profile":profile})

    def login_user(request):
        if request.method == "POST":
            username=request.POST['username']
            password=request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                #load cart contents from DB
                current_user = Profile.objects.get(user__id=request.user.id)
                user_cart = current_user.old_cart

                #convert str to dict
                if user_cart:
                    user_cart_json = json.loads(user_cart)
                
                cart = Cart(request)
                # add items from db to Cart
                for key, value in user_cart_json.items():
                    cart.add_from_db(product=key, quantity=value)

                messages.success(request, ("You have been logged in"))
                return redirect('home')
            else:
                messages.success(request, ("Wrong password or username"))
                return redirect('login')
        else:
            return render(request, 'profile/login.html', {})


    def logout_user(request):
        logout(request)
        messages.success(request, ("You have been logged out"))
        return redirect('home')

    def register_user(request):
        form = SignUpForm()
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                
                # Log in user
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, ("You have successfully registered"))
                return redirect('home')
            
        return render(request, 'profile/register.html', {'form':form})

    def update_user(request):
        if request.user.is_authenticated:
            current_user = Profile.objects.get(user__id=request.user.id)
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            # Get Forms
            user_form = UpdateUserForm(request.POST or None, instance=current_user)
            user_info = UserInfoForm(request.POST or None, instance=current_user)
            shipping_address_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

            if user_info.is_valid() or shipping_address_form.is_valid() or user_form.is_valid():
                #save user info
                if user_form.is_valid():
                    user_info.save()
                #save shipping address
                if shipping_address_form.is_valid():
                    shipping_address_form.save()

                if user_form.is_valid():
                    user_form.save()
                messages.success(request, ("Profil został zaktualizowany!"))
                return redirect(request.META.get("HTTP_REFERER"))
            
            

            return render(request, "profile/update_user.html", {'current_user':current_user, 'shipping_user':shipping_user, 'user_form':user_form, 'user_info':user_info, 'shipping_address_form':shipping_address_form})
        else:
            messages.success(request, ("You Must Be Logged In To View That Page..."))
            return redirect('home')
        
    def delete_user(request):
        if request.user.is_authenticated:
            del_user = User.objects.get(id=request.user.id)
            del_user.delete()
            messages.success(request, ("Your Profile Has Been Deleted!"))
            return redirect('home')

#change password
class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    template_name = 'profile/change_password.html'
    success_message = "Password has been changed!"   

#search product
class SearchView(APIView):
    renderer_classes= [TemplateHTMLRenderer]
    template_name = 'product/search.html'

    def post(self, request):
        featured = FeaturedProducts.objects.all()
        categories = Category.objects.all()
        if request.method == "POST":
                #grab search phrase
            search = request.POST['search']
            searched_category = request.POST['category']
            search_result = ''
            if searched_category == 'wszystkie-kategorie':
                search_result = Product.objects.filter(title__contains=search)
            elif Category.objects.get(name=searched_category):
                
                search_result = Product.objects.filter(category__parent_name__name=searched_category).filter(title__contains=search)
            else:
                messages.success(request, ("Brak produktów w podanej kategorii"))
            return Response({'search_result':search_result,'featured_products':featured, 'categories':categories})    

#single item view        
class SingleProductView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/p_single.html'

    def get(self, request, slug, pk):
        single_product = None

        if pk:
            single_product = Product.objects.get(id=pk)
            
        return Response({'single_product':single_product})
    
#category view - list subcategories
class CategoryView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/p_category.html'

    def get(self, request, slug, pk):
        category = None
        
        if pk:
            category = Subcategory.objects.filter(parent_name=pk)
        return Response({'category':category})

#list subcategory items
class SubcategoryView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/p_subcategory.html'

    def get(self, request, slug, pk):
        subcategory = None
        if pk:
            subcategory = Product.objects.filter(category__id=pk)
        return Response({'subcategory':subcategory})