from django.urls import path

from .views import AnalysisCreateView, AnalysisDetailView, AnalysisListView

urlpatterns = [
    path('', AnalysisListView.as_view(), name='analysis-list'),
    path('create/', AnalysisCreateView.as_view(), name='analysis-create'),
    path('<int:pk>/', AnalysisDetailView.as_view(), name='analysis-detail'),
]
