from django.shortcuts import render
from itertools import product

from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from products.models import Product, Category
from cart.models import Cart, CartItem
from cart.forms import AddToCartForm

# Create your views here.
# def cart_view(request):
# def cart_add(request, product_id):
# def cart_update(request, item_id):
# def cart_remove(request, item_id):
def get_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            return Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            pass
    cart = Cart.objects.create()
    request.session['cart_id'] = cart.id
    return cart

def cart_view(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart).select_related('product')
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # out of stock check before even showing the form
    if not product.is_available or product.stock == 0:
        messages.error(request, "This product is out of stock.")
        return redirect('product_detail', pk=product_id)

    form = AddToCartForm(request.POST or None, product=product)

    if request.method == 'POST' and form.is_valid():
        quantity = form.cleaned_data['quantity']
        cart = get_cart(request)

        # if item already in cart, add to existing quantity
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            new_quantity = item.quantity + quantity
            # check again that combined quantity doesn't exceed stock
            if new_quantity > product.stock:
                messages.error(request, f"You already have {item.quantity} in your cart. Only {product.stock} available.")
                return redirect('cart_view')
            item.quantity = new_quantity
        else:
            item.quantity = quantity
        item.save()

        messages.success(request, f"{product.name} added to cart.")
        return redirect('cart_view')

    return render(request, 'cart_add.html', {'form': form, 'product': product})


def cart_update(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    form = AddToCartForm(request.POST or None, product=item.product)

    if request.method == 'POST' and form.is_valid():
        item.quantity = form.cleaned_data['quantity']
        item.save()
        messages.success(request, "Cart updated.")
        return redirect('cart_view')

    return render(request, 'cart_update.html', {'form': form, 'item': item})


def cart_remove(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_view')