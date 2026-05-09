from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerView, CustomerDebtsView, DebtPaymentView

router = DefaultRouter()
router.register(r'customers', CustomerView)
router.register(r'customer-debts', CustomerDebtsView)
router.register(r'debt-payments', DebtPaymentView)

urlpatterns = [
    path('', include(router.urls)),
]