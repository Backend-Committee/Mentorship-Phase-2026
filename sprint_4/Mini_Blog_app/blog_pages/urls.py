from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home, name='home'),
    path('blog_list', views.BlogList, name='blog_list'),
    path('blog/<int:blog_id>', views.BlogDetail, name='blog_detail'),
]