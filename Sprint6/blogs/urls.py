from django.urls import path

from . import views

urlpatterns = [
    path('', views.BlogsListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', views.BlogsDetailView.as_view(), name='blog_detail'),
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('follow-toggle/', views.FollowToggle.as_view(), name='follow_toggle'),
    path('edit/<slug:slug>/', views.BlogEditView.as_view(), name='blog_edit'),
    path('delete/<slug:slug>/', views.BlogDeleteView.as_view(), name='blog_delete'),
]
