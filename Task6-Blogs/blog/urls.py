from django.urls import path

from . import views

app_name = 'blog'

urlpatterns =[
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    # new should be befor slug, otherwise it would try to match new as a slug
    path('blog/new/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:slug>/edit/', views.BlogUpdateView.as_view(), name='blog_edit'),
    path('blog/<slug:slug>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
]