from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from koszyk.cart import Cart
from kasa.forms import ShippingAddressForm, CardPaymentForm
from kasa.models import ShippingAddress, ShippingMethod, PaymentMethods, Order, OrderItems
from rynek.models import Profile

from django.contrib.auth.models import Group

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
        payment_methods = PaymentMethods.objects.all()

        payment_form = CardPaymentForm(request.POST or None)
        shipping_cost = ShippingMethod.objects.get(methods=2).price
        total = shipping_cost + cart_total
        if request.user.is_authenticated:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_address_form = ShippingAddressForm(request.POST or None, instance=shipping_user)
            return Response({'cart_checkout':cart_checkout, 'cart_quantities':cart_quantities, 'cart_total':cart_total, 'cart_subtotal':cart_subtotal, 'shipping_address_form':shipping_address_form, 'shipping_user':shipping_user, 'shipping_methods':shipping_methods, 'total':total, 'payment_methods':payment_methods, 'payment_form':payment_form})
        else:
            shipping_address_form = ShippingAddressForm(request.POST or None)
            return Response({'cart_checkout':cart_checkout, 'cart_quantities':cart_quantities, 'cart_total':cart_total, 'cart_subtotal':cart_subtotal, 'shipping_address_form':shipping_address_form, 'shipping_methods':shipping_methods, 'total':total, 'payment_methods':payment_methods, 'payment_form':payment_form})
        
    def shipping(request):
        cart = Cart(request)
        # Get items total price
        cart_total = cart.get_cart_total()
        
        if request.POST.get('action') == 'post':
            shipping_method = int(request.POST.get('shipping'))
            shipping_cost = ShippingMethod.objects.get(methods=shipping_method).price
            total = shipping_cost + cart_total
            
            #return response
            response = JsonResponse({'shipping_cost': shipping_cost, 'total':total})
            return response
        else:
            messages.success(request, ("Niedozwolona akcja"))
            return redirect('home')
        
    def payment(request):
        pass

    def process_order(request):
        post_data = request.POST
        #Grab items for Order model 
        """
        - order_user, 
        - order_full_name (name and surname), 
        - order_email, 
        - order_shipping_address, 
        - order_amount_paid, 
        """
        if post_data:
            
            # Get the cart items 
            cart = Cart(request)
            cart_products = cart.get_products
            cart_quantities = cart.get_quantity

            #Get cart total costs
            cart_total = cart.get_cart_total()

            shipping = int(post_data.get('shippingMethod'))

            # Get shipping method
            shipping_method = ShippingMethod.objects.get(methods=shipping).get_methods_display()

            # Get shipping costs
            shipping_cost = ShippingMethod.objects.get(methods=shipping).price
            
            # Calculate total costs
            total = shipping_cost + cart_total

            # Get payment method
            #payment_method = int(post_data.get('paymentMethod'))
            
            print(total)
            # Get order data
            if request.user.is_authenticated:
                # Get order_user
                user = request.user

                shipping_address = ShippingAddress.objects.get(user__id=request.user.id)
                # Get order_full_name
                full_name = shipping_address.shipping_full_name

                # Get order_email
                email = shipping_address.shipping_email
                # Get order_shipping_address
                address = f"{shipping_address.shipping_house_and_street_no}\n{shipping_address.shipping_postal_code} {shipping_address.shipping_city}\n{shipping_address.shipping_country}"

                # Create order
                create_order = Order(order_user=user, order_full_name=full_name, order_email=email, order_shipping_address=address, order_amount_paid=total, order_shipping_method=shipping_method)
                create_order.save()

                # Get order id
                order_id = create_order.pk
                
                for product in cart_products():
                    # Get product id
                    product_id = product.id
                    
                    # Get product price (or sale price)
                    if product.is_on_sale:
                        price = product.price_on_sale
                    else:
                        price = product.price

                    # Get quantity and create orderItem
                    for key, value in cart_quantities().items():
                        if int(key) == product.id:
                            create_order_items = OrderItems(items_order_id=order_id, items_product_id=product_id, items_user=user, items_quantity=value, items_price=price)
                            create_order_items.save()
                    
                # Delete cart from session and from profile (db)
                for key in list(request.session.keys()):
                    if key == "session_key":
                        del request.session[key]
                current_user = Profile.objects.filter(user__id=request.user.id)
                current_user.update(old_cart="")

            else:
                # order_user = null

                # Get order_full_name
                full_name = post_data['shipping_full_name']

                # Get order_email
                email = post_data['shipping_email']
                # Get order_shipping_address
                address = f"{post_data['shipping_house_and_street_no']}\n{post_data['shipping_postal_code']} {post_data['shipping_city']}\n{post_data['shipping_country']}"
                
                # Create order
                create_order = Order(order_full_name=full_name, order_email=email, order_shipping_address=address, order_amount_paid=total, order_shipping_method=shipping_method)
                create_order.save()
                
                # Get order id
                order_id = create_order.pk
                
                for product in cart_products():
                    # Get product id
                    product_id = product.id
                    
                    # Get product price (or sale price)
                    if product.is_on_sale:
                        price = product.price_on_sale
                    else:
                        price = product.price

                    # Get quantity and create orderItem
                    for key, value in cart_quantities().items():
                        if int(key) == product.id:
                            create_order_items = OrderItems(items_order_id=order_id, items_product_id=product_id, items_quantity=value, items_price=price)
                            create_order_items.save()
                
                # Delete cart from session
                for key in list(request.session.keys()):
                    if key == "session_key":
                        del request.session[key]

            return redirect('order_placed')

        else:
            messages.success(request, ("Niedozwolona akcja"))
            return redirect('home')
        
class OrderPlacedView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'kasa/order_placed.html'

    def get(self, request):
        
        return Response({})
        