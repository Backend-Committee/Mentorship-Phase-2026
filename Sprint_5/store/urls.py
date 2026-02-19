from django.urls import path
from . import views

urlpatterns = [
    path('',views.product, name ='products'),

    path('add_product/',views.add_product, name ='add_product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart, name ='cart'),

]