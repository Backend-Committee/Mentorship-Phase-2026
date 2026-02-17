from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.db.models import F
from cart.models import Cart
from .models import Payment
from order.models import Order, OrderItem

@login_required
@transaction.atomic
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitems.all().select_related('product')

    if request.method == 'POST':
        # 1. Validate Stock first
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(request, f"Sorry, {item.product.name} is out of stock (Only {item.product.stock} left).")
                return redirect('cart_view')

        # 2. Process Payment
        amount = cart.total_price()
        payment_method = request.POST.get('method')
        shipping_address = request.POST.get('shipping_address', request.user.address)
        
        payment = Payment.objects.create(
            user=request.user, 
            amount=amount, 
            method=payment_method, 
            status='completed'
        )
        
        # 3. Create Order
        order = Order.objects.create(
            user=request.user, 
            payment=payment, 
            status='pending',
            shipping_address=shipping_address
        )
        
        # 4. Create Order Items and Deduct Stock safely
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
                status='pending'  # Initial status for the item
            )
            # Use F() expression to avoid race conditions
            item.product.stock = F('stock') - item.quantity
            item.product.save()

        # 5. Clear Cart
        cart.clear_cart()
        return redirect('payment_success')
        
    return render(request, 'payment/checkout.html', {'cart': cart})

def payment_success(request):
    return render(request, 'payment/success.html')
