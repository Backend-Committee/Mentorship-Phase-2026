from django.urls import path

from .views import ExtractionTaskDetailView, ExtractionTaskListCreateView

urlpatterns = [
    path('', ExtractionTaskListCreateView.as_view(), name='extraction-list'),
    path('<int:pk>/', ExtractionTaskDetailView.as_view(), name='extraction-detail'),
]
