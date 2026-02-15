from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    HttpRequest,
)
from django.urls import reverse
from .models import Product
from .forms import CartItemForm
from django.forms import formset_factory


def home_view(request):
    context = {"products": Product.objects.select_related().all()}
    return render(request, "home.html", context=context)


def product_view(request: HttpRequest, product_id):
    try:
        product = Product.objects.select_related().get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound(
            f"<h1>No product with id = {product_id} exists!</h1>"
        )

    error = None
    if request.method == "POST":
        form = CartItemForm(request.POST)
        if form.is_valid():
            old_quantity = request.session.get(f"cart_{product_id}", 0)
            quantity = form.cleaned_data["quantity"]
            request.session[f"cart_{product_id}"] = min(
                old_quantity + quantity, product.stock
            )
            print(request.session.items())
            return HttpResponseRedirect(reverse("cart"))
        else:
            error = "Quantity must be bigger than or equal 1!"

    form = CartItemForm(initial={"quantity": 1})
    context = {"product": product, "form": form, "error": error}
    return render(request, "product.html", context=context)


def cart_view(request: HttpRequest):
    if request.method == "POST":
        for key in request.POST:
            print(key)
            print()
        
    initial = []
    products_ids = []
    for key, value in request.session.items():
        products_ids.append(int(key.split("_")[1]))
        initial.append({"quantity": value})
    products = Product.objects.select_related().filter(id__in=products_ids).all()
    context = {'initial': initial, "products": products}
    return render(request, "cart.html", context=context)
