from django.urls import path

from . import views

app_name = 'blog'

urlpatterns =[
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('category/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
]