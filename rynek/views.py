from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product

class StraganView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'
    
    def get(self, request):
        products = Product.objects.all()
        return Response({'products':products})
    
