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
    
    def add(self, product):
        product_id = str(product)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'cena': str(product.price)}
        
        self.session.modified = True

    def __len__(self):
        return len(self.cart)