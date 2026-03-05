from django.urls import path
from .views import deposit, Withdraw

urlpatterns = [
    path("deposit/", deposit, name="deposit"),
    path("withdraw/", Withdraw.as_view(), name="withdraw"),
    
]
