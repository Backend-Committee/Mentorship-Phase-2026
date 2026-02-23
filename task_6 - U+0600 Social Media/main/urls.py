from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.PostList.as_view(), name="post_list"),
    path('post/<str:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('create_post/', views.PostCreate.as_view(), name='post_create'),
    path('update_post/<str:pk>/', views.PostUpdate.as_view(), name='post_update'),
    path('delete_post/<str:pk>/', views.PostDelete.as_view(), name='post_delete'),
]
