from .cart import Cart

#create context processor so that our app can work
def cart(request):
    #return default data from cart

    return {'cart':Cart(request)}