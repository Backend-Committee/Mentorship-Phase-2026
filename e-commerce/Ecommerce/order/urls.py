from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('update-item/<int:item_id>/<str:status>/', views.update_order_item_status, name='update_order_item_status'),
]
