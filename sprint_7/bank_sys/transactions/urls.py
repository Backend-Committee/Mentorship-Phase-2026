from django.urls import path
from .views import TransactionsListCreate, TransactionDetail

urlpatterns = [
    path('transactions/', TransactionsListCreate.as_view()),
    path('transactions/<int:pk>/', TransactionDetail.as_view()),
]