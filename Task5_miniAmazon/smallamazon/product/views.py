from django.shortcuts import render, get_object_or_404, redirect
from .models import product, login, Category
from .form import AddPro
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        passw = request.POST.get('password')
        if user:
            u = login.objects.create(username=user, password=passw)
            request.session['username'] = user
            request.session['user_id'] = u.id
            return redirect('product_List')
    return render(request, 'pages/home.html')

def product_List(request):
    if 'username' not in request.session: return redirect('home')
    products = product.objects.all()
    query = request.GET.get('q')
    if query: products = products.filter(name__icontains=query)
    cat = request.GET.get('category')
    if cat: products = products.filter(category=cat)
    return render(request, 'pages/product.html', {'pro': products})

def addpro(request):
    if request.method == 'POST':
        form = AddPro(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_List')
    else: form = AddPro()
    return render(request, 'pages/AddPro.html', {'pro_add': form})

def Updatepro(request, pk):
    pro_instance = get_object_or_404(product, pk=pk)
    if request.method == 'POST':
        form = AddPro(request.POST, request.FILES, instance=pro_instance)
        if form.is_valid():
            form.save()
            return redirect('product_List')
    else: form = AddPro(instance=pro_instance)
    return render(request, 'pages/update.html', {'pro_add': form, 'product': pro_instance})

def delete_product(request, pk):
    get_object_or_404(product, pk=pk).delete()
    return redirect('product_List')

def add_to_cart(request, pk):
    pro = get_object_or_404(product, pk=pk)
    qty = int(request.POST.get('quantity', 1))
    if qty > pro.stock:
        messages.error(request, f"Sorry, only {pro.stock} left.")
        return redirect('product_List')
    pro.stock -= qty
    pro.save()
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + qty
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for p_id, qty in cart.items():
        p = get_object_or_404(product, pk=p_id)
        sub = p.price * qty
        total += sub
        items.append({'product': p, 'quantity': qty, 'subtotal': sub})
    return render(request, 'pages/cart.html', {'cart_items': items, 'total': total})