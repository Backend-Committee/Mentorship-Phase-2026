from django.urls import path
from .views import home_view, product_view, cart_view, delete_item_from_cart

urlpatterns = [
    path("", home_view, name="home"),
    path("product/<int:product_id>", product_view, name="product"),
    path("cart", cart_view, name="cart"),
    path(
        "delete_item_from_cart",
        delete_item_from_cart,
        name="delete_item_from_cart",
    ),
]
