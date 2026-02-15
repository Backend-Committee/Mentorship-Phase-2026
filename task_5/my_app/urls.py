from django.urls import path
from .views import home_view, product_view, cart_view

urlpatterns = [
    path('', home_view, name='home'),
    path('product/<int:product_id>', product_view, name='product'),
    path('cart', cart_view, name='cart')
]