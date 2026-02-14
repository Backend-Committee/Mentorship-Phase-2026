from django.shortcuts import render, redirect, get_object_or_404
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

        # Check if product is available and has enough stock
        if product.is_Available and product.stock >= quantity:
            # Create or update cart item
            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                defaults={'price': product.price, 'quantity': quantity}
            )
            if not created:
                # If item already exists, update quantity
                cart_item.quantity += quantity
                cart_item.save()

            # Optionally reduce stock
            product.stock -= quantity
            product.save()

    return redirect('product_list')

# Create your views here.
