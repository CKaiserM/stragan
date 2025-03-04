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
        cart = Cart(request)
        
        cart_summary = cart.get_products
        cart_quantities = cart.get_quantity
        cart_total = cart.get_cart_total
        cart_subtotal = cart.get_cart_subtotal
        return Response({'cart_summary':cart_summary, 'cart_quantities':cart_quantities, 'cart_total':cart_total, 'cart_subtotal':cart_subtotal})
        
    def add(request):
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            product = get_object_or_404(Product, id=product_id)


            #Save session
            cart.add(product=product, quantity=product_qty)
            cart_quantity = cart.__len__()

            #return response
            response = JsonResponse({'Nazwa produktu': product.title, "ilość":cart_quantity})
            
            return response

    def delete(request):
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            cart.delete(product=product_id)

            #return response
            response = JsonResponse({'Nazwa produktu': product_id})
            
            return response


    def update(request):
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))

            product_qty = int(request.POST.get('product_qty'))

            #Save session
            cart.update(product=product_id, quantity=product_qty)

            cart_quantity = cart.__len__()

            #return response
            response = JsonResponse({'Quantity': product_qty})
            
            return response