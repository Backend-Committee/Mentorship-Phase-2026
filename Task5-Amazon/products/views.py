from itertools import product

from django.shortcuts import render
# from products.models import Cart

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from .models import Product, Category
from cart.models import Cart, CartItem
from cart.forms import AddToCartForm

# def home(request):
    
#     cart_id = request.session.get('cart_id')
#     if cart_id: 
#         try:
#             cart = Cart.objects.get(id=cart_id)
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create()
#             request.session('cart_id', cart.id)
    
#     context ={
#         'products': Product.objects.all(),
#         'cart': cart
#     }
#     return render(request, 'home.html', context)

# ADD THIS VIEW to your views.py

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(
        is_available=True, stock__gt=0
    ).select_related('category').order_by('-id')[:8]  # latest 8 products

    return render(request, 'home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })
    

def product_list(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    # Search by name
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Filter by category
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category__id=category_id)

    # Show only available
    available_only = request.GET.get('available_only', '')
    if available_only:
        products = products.filter(is_available=True, stock__gt=0)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_id': category_id,
        'available_only': available_only,
    }
    return render(request, 'product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})




def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'product_search.html', context)

# def product_detail(request,pk):
# def product_add(request):
# def product_update(request, pk):
# def product_delete(request, pk):
# def cart_view(request):
# def cart_add(request, product_id):
# def cart_update(request, item_id):
# def cart_remove(request, item_id):