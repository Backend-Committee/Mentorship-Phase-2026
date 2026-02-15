from django.contrib import admin
from django.urls import include, path

from .views import redirect_catalog

urlpatterns = [
    path("", redirect_catalog),
    path("users/", include("user.urls")),
    path("catalog/", include("catalog.urls")),
    path("cart/", include("cart.urls")),
    path("admin/", admin.site.urls),
]
