from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShiftView, ExpenseView

router = DefaultRouter()
router.register(r'expenses', ExpenseView)
router.register(r'', ShiftView, basename='shift')

urlpatterns = [
    path('', include(router.urls)),
]