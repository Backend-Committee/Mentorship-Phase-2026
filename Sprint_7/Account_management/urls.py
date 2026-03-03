from django.urls import path
from . import views
urlpatterns = [
    path('accounts/', views.ListCreateAccount.as_view() ,name = 'accounts'),
    path('accounts/<int:pk>' , views.AccountDetail.as_view() , name='account-detail'),
    path('transactions/', views.ListCreateTransaction.as_view() , name='transactions'),
    path('transactions/<int:pk>' , views.TransactionDetail.as_view() , name='transaction-detail'),
]