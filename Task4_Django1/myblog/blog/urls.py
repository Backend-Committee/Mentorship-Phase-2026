from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog_list/', views.BlogList, name='blog_list'),
    path('blog_details/<int:id>/', views.BlogDetails, name='blog_details'),
]