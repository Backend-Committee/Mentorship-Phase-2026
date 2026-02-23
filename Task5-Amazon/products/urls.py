from django.contrib import admin
from django.urls import include, path
from products import views

urlpatterns = [
    path('', views.home, name='home'),
    # list would contain the filters and search 
    path('products/list', views.product_list, name='product_list'),
    path('products/search', views.product_search, name='product_search'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    # path('products/add/', views.product_add, name='product_add'),
    # path('products/<int:pk>/update/', views.product_update, name='product_update'),
    # path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # # Cart
    # path('cart/', views.cart_view, name='cart_view'),
    # path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    # path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    # path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
]
