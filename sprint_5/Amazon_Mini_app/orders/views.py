from django.shortcuts import render, redirect
from .models import *
from users.models import *
from products.models import *
# Create your views here.
def cart(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)

    order, created = Order.objects.get_or_create(user=user, completed=False)
    items = order.orderitem_set.all()
    context = {'items': items, 'order': order}
    return render(request, 'orders/cart.html', context)


def add_to_cart(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=user, completed=False)
    order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)

    if not item_created:
        order_item.quantity += 1
        order_item.save()

    return redirect('cart')

def remove_from_cart(request, item_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    order, created = Order.objects.get_or_create(user=user, completed=False)
    item = order.orderitem_set.get(id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


def checkout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)

    order, created = Order.objects.get_or_create(user=user, completed=False)
    items = order.orderitem_set.all()

    if request.method == 'POST':
        for item in items:
            item.product.quantity -= item.quantity
            item.product.save()
        order.completed = True
        order.save()
        return redirect('product_list')
    context = {'items': items, 'order': order}
    return render(request, 'orders/checkout.html', context)