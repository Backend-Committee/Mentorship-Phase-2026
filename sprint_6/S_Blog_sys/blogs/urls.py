from django.urls import path
from . import views
urlpatterns = [
    path('posts', views.PostListView.as_view(), name='list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='details'),
    path('create', views.PostCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='delete'),
]