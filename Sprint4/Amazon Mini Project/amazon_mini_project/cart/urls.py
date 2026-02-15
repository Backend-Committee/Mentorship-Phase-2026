from django.urls import path

from . import views

urlpatterns = [
    path("", views.CartListView.as_view()),
    path("cart-item/", views.CartItemView.as_view()),
]
