from store.models import Product
class Cart():
    def __init__(self,request):
        self.session=request.session

        #get the current session 
        cart=self.session.get('session_key')
        
        #if the user is new,create one
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}
        
        #make sure cart is available on all pages of site
        self.cart=cart
    
    def add(self,product,quantity):
        product_id=str(product.id)
        product_qty=str(quantity)

        if product_id in self.cart:
            pass
        else:
           self.cart[product_id]={'price':str(product.price)}
           self.cart[product_id]=int(product_qty)        
        self.session.modified = True
    
    def __len__(self):
        return len(self.cart)
    

    def get_prods(self):
        #get ids from cart
        product_ids=self.cart.keys()        
        #use ids to lookup products in database model
        products=Product.objects.filter(id__in=product_ids)
        #return those products
        return products
    
    def get_quants(self):
        quantities=self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id=str(product)
        product_qty=int(quantity)

        ourcart=self.cart
        ourcart[product_id]=product_qty
        self.session.modified = True

        thing=self.cart

        return thing
    
    def delete(self,product):
        product_id=str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
    
    def cart_total(self):
        #get product ids
        product_ids=self.cart.keys()
        #lookup keys in product database
        products=Product.objects.filter(id__in=product_ids)

        quantities=self.cart
        #start loop from 0
        total=0
        for key,value in quantities.items():
            key=int(key)
            for product in products:
                if product.id==key:
                    if product.on_sale:
                       total+=(product.sale_price*value)
                    else:
                        total+=(product.price*value)
        return total    
    
    def clear(self):
        del self.session['session_key']
        self.session.modified = True