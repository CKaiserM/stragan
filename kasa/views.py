from django.http import JsonResponse

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from koszyk.cart import Cart
from kasa.forms import ShippingAddressForm
from kasa.models import ShippingAddress, ShippingMethod

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
        cart_total = cart.get_cart_total()
        cart_subtotal = cart.get_cart_subtotal()
        #add seller id!
        #shipping_methods = ShippingMethod.objects.filter(user__id=1)
        shipping_methods = ShippingMethod.objects.all()

        shipping_cost = ShippingMethod.objects.get(methods=2).price
        total = shipping_cost + cart_total
    
        if request.user.is_authenticated:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_address_form = ShippingAddressForm(request.POST or None, instance=shipping_user)
            return Response({'cart_checkout':cart_checkout, 'cart_quantities':cart_quantities, 'cart_total':cart_total, 'cart_subtotal':cart_subtotal, 'shipping_address_form':shipping_address_form, 'shipping_user':shipping_user, 'shipping_methods':shipping_methods, 'total':total})
        else:
            shipping_address_form = ShippingAddressForm(request.POST or None)
            return Response({'cart_checkout':cart_checkout, 'cart_quantities':cart_quantities, 'cart_total':cart_total, 'cart_subtotal':cart_subtotal, 'shipping_address_form':shipping_address_form, 'shipping_methods':shipping_methods, 'total':total})
        
    def shipping(request):
        cart = Cart(request)
        cart_total = cart.get_cart_total()
        
        if request.POST.get('action') == 'post':
            shipping_method = int(request.POST.get('shipping'))
            shipping_cost = ShippingMethod.objects.get(methods=shipping_method).price
            total = shipping_cost + cart_total
            #return response
            response = JsonResponse({'shipping_cost': shipping_cost, 'total':total})
            return response