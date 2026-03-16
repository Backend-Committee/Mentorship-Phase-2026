from django.urls import path
from .views import UserListCreate, UserDetails, AccountListCreate, AccountDetails

urlpatterns = [
    path('user/', UserListCreate.as_view()),
    path('user/<int:pk>/', UserDetails.as_view()),
    path('account/', AccountListCreate.as_view()),
    path('account/<int:pk>/', AccountDetails.as_view()),
]