from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .cart import Cart
from rynek.models import Product
from django.http import JsonResponse


class KoszykView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cart/c_summary.html'

    #get Cart summary
    def get(self, request):
        return Response({})
        
    def add(request):
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            
            product = get_object_or_404(Product, id=product_id)


            #Save session
            cart.add(product=product)

            cart_quantity = cart.__len__()

            #return response
            response = JsonResponse({'ilosc': cart_quantity})
            
            return response

    def delete(request):
        pass
    def update(request):
        pass    