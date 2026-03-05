from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views
from .views import (
    PostListView,
    RegisterView,
    createView,
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    createView,
)

urlpatterns = [
    # for login,logout
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/Register/", RegisterView.as_view(), name="register"),
    path("", PostListView.as_view(), name="blogs"),
    path("blog/<int:pk>/", PostDetailView.as_view(), name="blog-detail"),
    path("blog/<int:pk>/update/", PostUpdateView.as_view(), name="blog-update"),
    path("blog/<int:pk>/delete/", PostDeleteView.as_view(), name="blog-delete"),
    path("createView", createView.as_view(), name="createView"),
]