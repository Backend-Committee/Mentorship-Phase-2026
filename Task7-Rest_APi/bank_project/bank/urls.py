from django.urls import path
from .views import *

urlpatterns = [
    path("customers", get_customers),
    path("create-customer", create_customer),
    path("accounts", get_accounts),
    path("create-account", create_account),
    path("deposit", deposit),
    path("withdraw", withdraw),
    path("transfer", transfer),
]