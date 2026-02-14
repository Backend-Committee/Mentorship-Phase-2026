from django.urls import path
from . import views

urlpatterns = [
    path('', views.productItem, name='product' ),
    path('addCategory/', views.addCategory, name='add' ),
    path('products/', views.productList, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cartList, name='cart_list'),
]


