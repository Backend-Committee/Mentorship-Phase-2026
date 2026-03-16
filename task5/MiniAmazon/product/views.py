from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, CartItem
from .forms import ProductForm,AddCategoryForm

def productItem(request):
    if request.method == 'POST':
        data = ProductForm(request.POST)
        if data.is_valid():
            data.save()
    return render(request,'product/product.html',{'PF':ProductForm})
def addCategory(request):
    if request.method == 'POST':
        data = AddCategoryForm(request.POST)
        if data.is_valid():
            data.save()
    return render(request,'product/addCategory.html',{'ACF':AddCategoryForm})
def cartList(request):
    cardItems = CartItem.objects.select_related('product').all()
    context = {
        'cartItems': cardItems,
    }
    return render(request,'product/cartList.html',context)
def productList(request):
    pro = Product.objects.all()
    productContext = {'products':pro}
    return render(request,'product/productList.html',productContext)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        if not product.is_Available:
            messages.error(request, f'"{product.name}" is not available.')
        elif product.stock <= 0:
            messages.error(request, f'"{product.name}" is out of stock.')
        elif product.stock < quantity:
            messages.error(request, f'Only {product.stock} item(s) of "{product.name}" left in stock.')
        else:
            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                defaults={'price': product.price, 'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            product.stock -= quantity
            product.save()
            messages.success(request, f'"{product.name}" x{quantity} added to cart!')

    return redirect('product_list')

# Create your views here.
