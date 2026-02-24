from django.urls import path
from . import views
urlpatterns = [
    path('', views.BlogView.as_view(), name='index'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('new/', views.PostCreateView.as_view(), name='New_post'),
]
