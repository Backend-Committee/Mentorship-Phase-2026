from django.urls import path

from . import views
from .views import ProductView

urlpatterns = [
    path("products/", ProductView.as_view(), name="product_list"),
]
