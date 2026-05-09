from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineView, ShortageView

router = DefaultRouter()
router.register(r'medicines', MedicineView)
router.register(r'shortages', ShortageView)

urlpatterns = [
    path('', include(router.urls)),
]