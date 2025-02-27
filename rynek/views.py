from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

import after_response

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Profile, FeaturedProducts, Category
from .forms import SignUpForm, UpdateUserForm, AddressForm

class StraganView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'
    
    def get(self, request):
        products = Product.objects.all()
        featured = FeaturedProducts.objects.all()
        categories = Category.objects.all()
        return Response({'products':products, 'featured_products':featured, 'categories':categories})



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
            current_user = User.objects.get(id=request.user.id)
            profile_user = Profile.objects.get(user__id=request.user.id)
            # Get Forms
            user_form = UpdateUserForm(request.POST or None, instance=current_user)
            address_form = AddressForm(request.POST or None, instance=current_user)

            if user_form.is_valid():
                user_form.save()
                login(request, current_user)
                messages.success(request, ("Profil został zaktualizowany!"))
                return redirect('home')

            return render(request, "profile/update_user.html", {'user_form':user_form, 'address_form':address_form})
        else:
            messages.success(request, ("You Must Be Logged In To View That Page..."))
            return redirect('home')
        
    def delete_user(request):
        if request.user.is_authenticated:
            del_user = User.objects.get(id=request.user.id)
            del_user.delete()
            messages.success(request, ("Your Profile Has Been Deleted!"))
            return redirect('home')

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    template_name = 'profile/change_password.html'
    success_message = "Password has been changed!"   

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