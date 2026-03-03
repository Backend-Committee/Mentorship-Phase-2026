from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404
from .models import Transaction
from .serializers import TransactionSerializer
from accounts.models import Account
from approvals.models import ApprovalRequest
from audit.models import AuditLog
from users.permissions import IsCustomer, IsOfficeStaff, IsManager, IsAdmin
import decimal

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    # Adjust permission later
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == "CUSTOMER":
            return Transaction.objects.filter(account__user=user)
        # Assuming staff can see all for now, filter based on role logic
        return Transaction.objects.all()

    @db_transaction.atomic
    def create(self, request, *args, **kwargs):
        # Simplistic implementation structure
        data = request.data.copy() # Ensure mutable
        user = request.user
        
        try:
            amount_val = decimal.Decimal(data.get('amount'))
            transaction_type = data.get('transaction_type')
            account_id = data.get('account') 
            destination_account_id = data.get('destination_account')
        except (ValueError, TypeError):
             return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

        if amount_val <= 0:
            return Response({'error': 'Amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)

        source_account = get_object_or_404(Account, id=account_id)
        
        # Security: Customer can only transact on their own account
        if hasattr(user, 'role') and user.role == "CUSTOMER" and source_account.user != user:
             return Response({'error': 'Unauthorized account access'}, status=status.HTTP_403_FORBIDDEN)

        if source_account.is_frozen:
             return Response({'error': 'Account is frozen'}, status=status.HTTP_400_BAD_REQUEST)

        # Sufficient Funds Check
        if transaction_type in [Transaction.TransactionType.WITHDRAWAL, Transaction.TransactionType.TRANSFER]:
            if source_account.balance < amount_val:
                 return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        # High Value Check (> 50,000)
        is_large = amount_val > 50000
        is_transfer_withdrawal = transaction_type in [Transaction.TransactionType.WITHDRAWAL, Transaction.TransactionType.TRANSFER]

        if is_large and is_transfer_withdrawal:
             # Create PENDING transaction
             txn = Transaction.objects.create(
                 account=source_account,
                 destination_account_id=destination_account_id,
                 transaction_type=transaction_type,
                 amount=amount_val,
                 status=Transaction.TransactionStatus.PENDING,
                 description=data.get('description', '')
             )
             # Create Approval Request
             ApprovalRequest.objects.create(
                 transaction=txn,
                 requested_by=user,
                 status=ApprovalRequest.ApprovalStatus.PENDING
             )
             
             AuditLog.objects.create(
                 user=user,
                 action=f"INITIATED_LARGE_{transaction_type}",
                 details={'amount': str(amount_val), 'transaction_id': txn.id}
             )
             
             return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)

        # Normal Execution
        txn = Transaction.objects.create(
             account=source_account,
             destination_account_id=destination_account_id,
             transaction_type=transaction_type,
             amount=amount_val,
             status=Transaction.TransactionStatus.COMPLETED,
             description=data.get('description', '')
        )

        # Balance Updates
        if transaction_type == Transaction.TransactionType.DEPOSIT:
            source_account.balance += amount_val
            source_account.save()
            
        elif transaction_type == Transaction.TransactionType.WITHDRAWAL:
            source_account.balance -= amount_val
            source_account.save()
            
        elif transaction_type == Transaction.TransactionType.TRANSFER:
            source_account.balance -= amount_val
            source_account.save()
            if destination_account_id:
                dest_acc = get_object_or_404(Account, id=destination_account_id)
                dest_acc.balance += amount_val
                dest_acc.save()

        # Log
        AuditLog.objects.create(
            user=user,
            action=f"COMPLETED_{transaction_type}",
            details={'amount': str(amount_val), 'transaction_id': txn.id, 'new_balance': str(source_account.balance)}
        )

        return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)

