from django.shortcuts import render
from .models import Product, Category


def product_list(request):
    products = Product.objects.all().exclude(quantity=0).exclude(available=False)
    categories = Category.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(title__icontains=search_query)

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/List.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'products/product.html', context)