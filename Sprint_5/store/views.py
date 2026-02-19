from django.shortcuts import render
from .models import Product , Category


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return redirect('products')


def validate_price(price):
    index = price.find('.')
    if index == -1:
        if len(price) > 8:
            return False
        else:
            return True
    else:
        if len(price[:index]) > 8 or len(price[index+1:]) > 2:
            return False
        else:
            return True

def product(request):
    products= Product.objects.all()
    selected_cate = request.GET.get('category')
    if selected_cate: # selected category
        products_to_view = products.filter(category_id = int(selected_cate))
    else:
        products_to_view = products
    context = {
        'products_to_view': products_to_view,
        'categories': Category.objects.all(),
        'selected_category': int(selected_cate) if selected_cate else None,
    }
    return render(request , 'products.html' , context)

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        if not product_name or not price or not category or not description:
            return render(request, 'add_product.html', {'error': 'All fields are required.', 'categories': Category.objects.all()})
        if not validate_price(price):
            return render(request, 'add_product.html', {'error': 'Invalid price.', 'categories': Category.objects.all()})
        Product.objects.create(name=product_name, price=price, category_id=category, image=image, description=description)
    return render(request, 'add_product.html', {'categories': Category.objects.all()})


def cart(request):
    cart_items = request.session.get('cart', {})

    products_in_cart = []
    total = 0

    for product_id, quantity in cart_items.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal
            products_in_cart.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue

    context = {
        'products_in_cart': products_in_cart,
        'total': total
    }

    return render(request, 'cart.html', context)