from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r"staff", StaffViewSet)
router.register(r"customer", CustomerViewSet)
router.register(r"account-type", AccountTypeViewSet)
router.register(r"account", AccountViewSet)

urlpatterns = [
    path("", include(router.urls))
]