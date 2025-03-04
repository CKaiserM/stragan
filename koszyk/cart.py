from rynek.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        #Get the current session key
        cart = self.session.get('session_key')

        #if no session key, create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make cart available on all pages
        self.cart = cart
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        print(product_qty)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True

    def update(self, product, quantity):
        
        product_id = str(product)
        product_qty = int(quantity)

        cart = self.cart

        cart[product_id] = product_qty

        self.session.modified = True

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def get_cart_total(self):
        product_ids = self.cart.keys()
        #filter cart products by ids.
        products_in_carts = Product.objects.filter(id__in=product_ids)
        cart_qts = self.cart

        total = 0

        for key, value in cart_qts.items():
            key = int(key)
            for product in products_in_carts:
                if product.id == key:
                    total = total + (product.price * value)
        return total
    
    def get_cart_subtotal(self):
        product_ids = self.cart.keys()
        #filter cart products by ids.
        products_in_carts = Product.objects.filter(id__in=product_ids)
        #get cart items and qts
        cart_qts = self.cart
        #copy cart items
        subtotal = cart_qts.copy()
        
        #
        for key, value in subtotal.items():
            key = int(key)
            for product in products_in_carts:
                if product.id == key:
                    # multiply product price by qty and modify dict.
                    subtotal[str(key)] = (value * product.price)
        return subtotal

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        #get all keys (ids from self.cart[product_id])
        product_ids = self.cart.keys()
        products_in_cart = Product.objects.filter(id__in=product_ids)
        #return all
        return products_in_cart
    
    def get_quantity(self):
        quantity = self.cart
        return quantity
    
    




    

    
    