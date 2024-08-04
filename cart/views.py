from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import CheckoutForm
from .models import Order, OrderItem


def cart_summary(request):
    cart=Cart(request)
    cart_products=cart.get_prods
    quantities=cart.get_quants
    totals=cart.cart_total()
    return render(request,'cart_summary.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals})
def cart_add(request):
    ##get cart
    cart=Cart(request)
    #test for POST
    if request.POST.get('action') == 'post':
        #get stuff
        product_id=int(request.POST.get('product_id'))
        product_qty=int(request.POST.get('product_qty'))
        #lookup product in the database
        product=get_object_or_404(Product,id=product_id)
        #save to session
        cart.add(product=product,quantity=product_qty)
        #get cart quantity
        cart_quantity=cart.__len__()
        #return response
        #response=JsonResponse({'Product Name: ':product.name})

        response=JsonResponse({'qty':cart_quantity})
        messages.success(request,'Product Added to Cart...')

        return response


def cart_delete(request):
    cart=Cart(request)
    if request.POST.get('action') == 'post':
        #get stuff
        product_id=int(request.POST.get('product_id'))

        cart.delete(product=product_id)
        response=JsonResponse({'product':product_id})
        messages.success(request,'Product Has Been Deleted from Cart...')
        return response

def cart_update(request):
    cart=Cart(request)
    if request.POST.get('action') == 'post':
        #get stuff
        product_id=int(request.POST.get('product_id'))
        product_qty=int(request.POST.get('product_qty'))

        cart.update(product=product_id,quantity=product_qty)

        response=JsonResponse({'qty':product_qty})
        messages.success(request,'Cart Has Been Updated...')
        return response
        #return redirect('cart_summary')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.amount_paid = totals  # Assuming no initial payment
            order.save()

            # Save order items
            for product in cart_products:
                quantity = quantities[str(product.id)]
                price = product.sale_price if product.on_sale else product.price
                OrderItem.objects.create(
                    product=product,
                    order=order,
                    user=request.user if request.user.is_authenticated else None,
                    quantity=quantity,
                    price=price
                )

            # Send confirmation email
            send_mail(
                'Order Received',
                f'Thank you for your order, {order.full_name}. We will contact you soon.',
                'cyberjiutsu@gmail.com',  # Replace with your email
                [order.email],
                fail_silently=False,
            )

            # Clear the cart
            cart.clear()

            return redirect('order_confirmation')  # Redirect to a confirmation page
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'form': form
    })
def order_confirmation(request):
    return render(request, 'order_confirmation.html')