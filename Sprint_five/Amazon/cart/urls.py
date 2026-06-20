from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
    path('', views.view_cart, name='cart'),
]