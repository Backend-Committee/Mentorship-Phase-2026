from django.urls import path, include
from .views import register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("", include("django.contrib.auth.urls")),
]
