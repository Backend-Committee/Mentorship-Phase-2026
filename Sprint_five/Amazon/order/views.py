from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import OrderForm
from .models import OrderItem
from cart.models import CartItem
from main.models import Product

# Create your views here.

def order(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items,
    }

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            if total_items == 0:
                messages.error(request, "Your cart is empty. Please add items to your cart before placing an order.")
                return redirect('home')
            order = form.save(commit=False)
            order.total_price = total_price
            order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                product = Product.objects.get(id=item.product.id)
                product.stock -= item.quantity
                product.save()
            for item in cart_items:
                item.delete()
            messages.success(request, "Order placed successfully!")
            return redirect('home')

    else:
        form = OrderForm()

    return render(request, 'confirm.html', {
        'form': form,
        **context
    })
