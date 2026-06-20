from django.shortcuts import render
from .models import CartItem
from main.models import Product
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# Create your views here.


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart_item = CartItem.objects.create(product=product, quantity=1)
    return HttpResponse("""
<span style="color:green;">Added to cart ✔</span>
""")

def view_cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items,
    }
    return render(request, 'cart.html', context)

def remove_from_cart(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    return HttpResponse("""
<span style="color:red;">Removed from cart ✔</span>
""")

# views.py

from django.http import JsonResponse

def update_quantity(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id)
    action = request.POST.get("action")

    if action == "increase":
        if item.quantity < item.product.stock:
            item.quantity += 1
    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
    elif action == "set":
        try:
            new_qty = int(request.POST.get("quantity", item.quantity))
        except (TypeError, ValueError):
            new_qty = item.quantity
        item.quantity = max(1, min(new_qty, item.product.stock))

    item.save()

    cart_items = CartItem.objects.all()
    cart_total = sum(ci.product.price * ci.quantity for ci in cart_items)
    cart_total_items = sum(ci.quantity for ci in cart_items)

    return JsonResponse({
        "quantity": item.quantity,
        "line_total": float(item.product.price * item.quantity),
        "cart_total": float(cart_total),
        "cart_total_items": cart_total_items,
        "max_stock": item.product.stock,
        "at_max": item.quantity >= item.product.stock,
        "at_min": item.quantity <= 1,
    })