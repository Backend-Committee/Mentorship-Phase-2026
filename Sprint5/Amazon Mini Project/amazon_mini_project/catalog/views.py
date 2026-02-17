import json

from django.db.utils import IntegrityError
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from cart.models import CartItem
from catalog.models import Product
from user.models import User


@method_decorator(csrf_exempt, name="dispatch")
class ProductView(View):
    def get_quantity_for_product(self, user_id, product_id):
        u = User.objects.get(pk=user_id)
        p = Product.objects.get(pk=product_id)
        cartItem = CartItem.objects.get(product=p, user=u)
        return cartItem.quantity

    def get(self, request):
        request.session["user_id"] = 1
        all_products = Product.objects.all()

        user_id = request.session.get("user_id")
        if not user_id:
            return HttpResponseNotFound("User not found in session.")

        user = User.objects.get(pk=user_id)
        products_id_in_cart = CartItem.objects.filter(user=user).values_list(
            "product", flat=True
        )
        product_id_quantity = {
            id: self.get_quantity_for_product(user_id, id)
            for id in set(products_id_in_cart)
        }

        print(product_id_quantity)

        return render(
            request,
            "catalog/products_list.html",
            {"products": all_products, "product_id_quantity": product_id_quantity},
        )
