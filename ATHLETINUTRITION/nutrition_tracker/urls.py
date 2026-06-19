from django.urls import path
from . import views

urlpatterns = [
    path('', views.NutritionListView.as_view(), name='nutrition_list'),
    path('add/', views.NutritionCreateView.as_view(), name='nutrition_add'),
    path('edit/<int:pk>/', views.NutritionUpdateView.as_view(), name='nutrition_edit'),
    path('delete/<int:pk>/', views.NutritionDeleteView.as_view(), name='nutrition_delete'),
]