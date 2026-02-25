from django.urls import path
from .views import sign_up, login
urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('log-in/', login, name='login'),
]