from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import F
from django.urls import reverse
from .models import OrderItem

def is_owner(user):
    return user.is_authenticated and user.role == 'owner'

@user_passes_test(is_owner)
def owner_dashboard(request):
    # Get all order items for products owned by this user
    order_items = OrderItem.objects.filter(product__owner=request.user).order_by('-order__created_at')
    return render(request, 'order/owner_dashboard.html', {'order_items': order_items})

@user_passes_test(is_owner)
def update_order_item_status(request, item_id, status):
    item = get_object_or_404(OrderItem, id=item_id, product__owner=request.user)
    
    if status == 'cancelled' and item.status != 'cancelled':
        # Restore stock if cancelling
        item.product.stock = F('stock') + item.quantity
        item.product.save()
    elif status != 'cancelled' and item.status == 'cancelled':
        # Deduct stock if un-cancelling (re-activating)
        # Note: Need refresh_from_db to check actual stock first if we wantstrict check, but F() is safer for concurrent updates
        # If we use F(), we can't easily check condition in python. 
        # For simplicity in this demo, we'll just check current object's stock but use F for update.
        item.product.refresh_from_db()
        if item.product.stock >= item.quantity:
            item.product.stock = F('stock') - item.quantity
            item.product.save()
        else:
            messages.error(request, f"Not enough stock to reactivate order for {item.product.name}")
            return redirect('owner_dashboard')
            
    item.status = status
    item.save()
    return redirect('owner_dashboard')
