import sys
from django.urls import path
from BackEnd.Controller import authController

urlpatterns = [
    path('register', authController.register),
    path('login', authController.login),
]