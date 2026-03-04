from django.urls import path

from . import views

urlpatterns = [
    path('', views.BankListCreateView.as_view(), name='bank-list-create'),
    path('<int:pk>/', views.BankRetrieveUpdateDestroyView.as_view(), name='bank-retrieve-update-destroy'),
    path('<int:bank_id>/accounts/', views.BankAccountListCreateView.as_view(), name='bank-account-list-create'),
    path('accounts/<int:pk>/', views.BankAccountRetrieveUpdateDestroyView.as_view(), name='bank-account-retrieve-update-destroy'),
]
