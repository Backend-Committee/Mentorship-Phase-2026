from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign-up'),
    path('log-in/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]