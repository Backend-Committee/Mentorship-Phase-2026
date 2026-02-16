from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    HttpRequest,
)
from django.urls import reverse
from .models import Product, Category
from .forms import FilterForm, ItemQuantityForm, ItemQuantityFormSet
from django.forms import formset_factory
from django.db.models import F
from django.views.decorators.http import require_POST

def home_view(request: HttpRequest):
    categories = Category.objects.all()
    products = Product.objects.select_related()

    filter_form = FilterForm(
        request.GET,
        choices=[("", "All")]
        + [(category.id, category.name.capitalize()) for category in categories],
    )

    if filter_form.is_valid():
        if filter_form.cleaned_data["category"] != "":
            products = products.filter(category_id=filter_form.cleaned_data["category"])

        if filter_form.cleaned_data["available_only"]:
            products = products.filter(stock__gt=0)

        search = filter_form.cleaned_data["search"].strip()
        if search:
            products = products.filter(name__icontains=search)

    context = {
        "products": products.all(),
        "categories": categories,
        "filter_form": filter_form,
    }
    return render(request, "home.html", context=context)


def product_view(request: HttpRequest, product_id):
    try:
        product = Product.objects.select_related().get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound(
            f"<h1>No product with id = {product_id} exists!</h1>"
        )

    if request.method == "POST" and not product.is_available():
        return HttpResponseNotFound(f"<h1>This product is currently out of stock!</h1>")

    if request.method == "POST":
        request.session.setdefault("cart", [])
        request.session["cart"].append(product.id)
        request.session.save()
        return HttpResponseRedirect(reverse("cart"))

    return render(request, "product.html", context={"product": product})


def cart_view(request: HttpRequest):
    if request.POST:
        formset = ItemQuantityFormSet(request.POST, request.FILES)
        if formset.is_valid():
            product_ids = []
            for data in formset.cleaned_data:
                Product.objects.filter(id=data["product_id"]).update(
                    stock=F("stock") - data["quantity"]
                )
            request.session.pop('cart', None)
            return HttpResponse("<h1>Order has been placed successfully!</h1>")
        else:
            return HttpResponse("<h1>Finishing the order failed!</h1>")

    product_ids = sorted(request.session.get("cart", []))
    initial = []
    for product_id in product_ids:
        initial.append({"product_id": product_id})
    products = Product.objects.filter(id__in=product_ids).order_by("id").all()
    
    form_kwargs = {}
    for i in range(0, len(products)):
        form_kwargs[i] = {"stock": products[i].stock}

    formset = ItemQuantityFormSet(initial=initial, form_kwargs=form_kwargs)

    context = {"formset": formset, "products": products}
    return render(request, "cart.html", context=context)

@require_POST
def delete_item_from_cart(request: HttpRequest):
    product_id = int(request.POST.get('product_id', -1))
    if product_id in request.session.get('cart', []):
        new_cart = []
        for elem in request.session.get('cart'):
            if elem != product_id:
                new_cart.append(elem)
        request.session['cart'] = new_cart
        request.session.save()
    
    return HttpResponseRedirect(reverse('cart'))