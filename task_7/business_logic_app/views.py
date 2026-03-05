from django.db.models import F
from rest_framework import decorators, views
from rest_framework.response import Response
from .serializers import DepositSerializer, WithdrawSerializer
from .models import Transaction

@decorators.api_view(["POST"])
def deposit(request):
    deposit_serializer = DepositSerializer(data=request.data)
    
    deposit_serializer.is_valid(raise_exception=True)
    
    account = deposit_serializer.validated_data['account']
    amount = deposit_serializer.validated_data['amount']
    
    account.balance = F("balance") + amount
    account.save()
    
    transaction = Transaction(account=account, amount=amount, type=Transaction.DEPOSIT)
    transaction.save()
    
    return Response({"message": "deposit has been completed successfully"})

class Withdraw(views.APIView):
    def post(self, request, format=None):
        withdraw_serializer = WithdrawSerializer(data=request.data)
        
        withdraw_serializer.is_valid(raise_exception=True)
        
        account = withdraw_serializer.validated_data['account']
        amount = withdraw_serializer.validated_data['amount']
    
        account.balance = F("balance") - amount
        account.save()
        
        transaction = Transaction(account=account, amount=amount, type=Transaction.WITHDRAWAL)
        transaction.save()

        return Response({"message": "withdrawal has been completed successfully"})
        