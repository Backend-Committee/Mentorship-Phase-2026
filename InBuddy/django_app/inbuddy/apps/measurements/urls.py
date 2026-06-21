from django.urls import path

from .views import MeasurementDetailView, MeasurementLatestView, MeasurementListCreateView

urlpatterns = [
    path('', MeasurementListCreateView.as_view(), name='measurement-list'),
    path('latest/', MeasurementLatestView.as_view(), name='measurement-latest'),
    path('<int:pk>/', MeasurementDetailView.as_view(), name='measurement-detail'),
]
