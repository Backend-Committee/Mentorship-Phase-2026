from django.shortcuts import render
from rest_framework import generics
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
# Create your views here.

#CREATE
class ListCreateAccount(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        customer_id = self.request.data.get('customer')  # من POST data
        account_type = self.request.data.get('account_type')
        balance = self.request.data.get('balance', 0)

        account, created = Account.objects.get_or_create(
            customer_id=customer_id,
            account_type=account_type,
            defaults={'balance': balance}
        )
        serializer.save(customer_id=customer_id)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DeleteAccount(generics.DestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ListCreateTransaction(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer