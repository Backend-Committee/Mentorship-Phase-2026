from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceView, InvoiceItemView

router = DefaultRouter()
router.register(r'invoices', InvoiceView)
router.register(r'invoice-items', InvoiceItemView)

urlpatterns = [
    path('', include(router.urls)),
]