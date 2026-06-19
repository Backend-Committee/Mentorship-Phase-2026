from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkoutListView.as_view(), name='workout_list'),
    path('add/', views.WorkoutCreateView.as_view(), name='workout_add'),
    path('edit/<int:pk>/', views.WorkoutUpdateView.as_view(), name='workout_edit'),
    path('delete/<int:pk>/', views.WorkoutDeleteView.as_view(), name='workout_delete'),
]