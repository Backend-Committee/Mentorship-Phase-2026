from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Customer, BankAccount, Transaction
from .serializers import (
    CustomerSerializer, BankAccountSerializer,
    DepositWithdrawSerializer, TransferSerializer, TransactionSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset           = Customer.objects.all()
    serializer_class   = CustomerSerializer


class BankAccountViewSet(viewsets.ModelViewSet):
    queryset           = BankAccount.objects.all()
    serializer_class   = BankAccountSerializer

    # POST /accounts/{id}/deposit/
    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        account = get_object_or_404(BankAccount, pk=pk)
        serializer = DepositWithdrawSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, type='deposit', amount=amount)
        return Response({'message': 'Deposit successful', 'new_balance': account.balance})

    # POST /accounts/{id}/withdraw/
    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        account = get_object_or_404(BankAccount, pk=pk)
        serializer = DepositWithdrawSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data['amount']
        if account.balance < amount:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, type='withdrawal', amount=amount)
        return Response({'message': 'Withdrawal successful', 'new_balance': account.balance})

    # POST /accounts/{id}/transfer/
    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        from_account = get_object_or_404(BankAccount, pk=pk)
        serializer = TransferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount     = serializer.validated_data['amount']
        to_account = get_object_or_404(BankAccount, pk=serializer.validated_data['to_account_id'])

        if from_account.balance < amount:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
        if from_account == to_account:
            return Response({'error': 'Cannot transfer to the same account'}, status=status.HTTP_400_BAD_REQUEST)

        from_account.balance -= amount
        to_account.balance   += amount
        from_account.save()
        to_account.save()
        Transaction.objects.create(account=from_account, type='transfer', amount=amount, to_account=to_account)
        return Response({'message': 'Transfer successful', 'new_balance': from_account.balance})