from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, BankAccountViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'accounts',  BankAccountViewSet)

urlpatterns = router.urls