import json

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from cart.models import CartItem
from catalog.models import Product
from user.models import User


@method_decorator(csrf_exempt, name="dispatch")
class CartItemView(View):
    def post(self, request):
        body = request.body.decode("utf-8")
        bodyData = json.loads(body)

        try:
            user_id = request.session.get("user_id")
            if not user_id:
                return HttpResponseNotFound("User not found in session.")
            u = User.objects.get(pk=user_id)
            p = Product.objects.get(pk=bodyData["productId"])

            CartItem.objects.create(product=p, user=u)
            return HttpResponse("Item created successfully", status=201)
        except User.DoesNotExist:
            return HttpResponseNotFound("User Not Found")

    def patch(self, request):
        body = request.body.decode("utf-8")
        bodyData = json.loads(body)

        try:
            user_id = request.session.get("user_id")
            if not user_id:
                return HttpResponseNotFound("User not found in session.")
            u = User.objects.get(pk=user_id)
            p = Product.objects.get(pk=bodyData["productId"])
            q = bodyData["quantity"]

            c = CartItem.objects.get(product=p, user=u)
            c.quantity = q
            c.save()
            return HttpResponse("quantity changed successfully", status=200)
        except User.DoesNotExist:
            return HttpResponseNotFound("User Not Found")
        except Product.DoesNotExist:
            return HttpResponseNotFound("Product Not Found")
        except CartItem.DoesNotExist:
            return HttpResponseNotFound("Product does not added to cart!")

    def delete(self, request):
        body = request.body.decode("utf-8")
        bodyData = json.loads(body)

        try:
            user_id = request.session.get("user_id")
            if not user_id:
                return HttpResponseNotFound("User not found in session.")
            u = User.objects.get(pk=user_id)
            p = Product.objects.get(pk=bodyData["productId"])

            cart_item = CartItem.objects.get(product=p, user=u)
            cart_item.delete()
            return HttpResponse("Item deleted successfully", status=204)
        except User.DoesNotExist:
            return HttpResponseNotFound("User Not Found")
        except Product.DoesNotExist:
            return HttpResponseNotFound("Product Not Found")
        except CartItem.DoesNotExist:
            return HttpResponseNotFound("Product does not added to cart!")


class CartListView(View):
    def is_in_cart(self, product_id):
        try:
            cartItem = CartItem.objects.get(pk=product_id)
            return cartItem.quantity
        except CartItem.DoesNotExist:
            return 0

    def add_to_cart(self, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            CartItem.objects.create(product=product, user=self.u)
        except Product.DoesNotExist:
            return HttpResponseNotFound("Not Product exists with this id")

    def get(self, request):
        u = request.session.get("user_id")
        cartItems = CartItem.objects.filter(user=u)
        total = sum(item.product.price * item.quantity for item in cartItems)

        return render(
            request,
            "cart/cart.html",
            {
                "cartItems": cartItems,
                "total": total,
            },
        )
