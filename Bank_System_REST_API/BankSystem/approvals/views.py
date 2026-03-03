from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import ApprovalRequest
from .serializers import ApprovalRequestSerializer
from transactions.models import Transaction
from accounts.models import Account
from audit.models import AuditLog
from users.permissions import IsManager, IsAdmin

class ApprovalRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ApprovalRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager | IsAdmin]

    def get_queryset(self):
        # Managers see all pending or processed
        return ApprovalRequest.objects.all()

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def approve(self, request, pk=None):
        approval = self.get_object()
        
        if approval.status != ApprovalRequest.ApprovalStatus.PENDING:
            return Response({'error': 'Request already processed'}, status=status.HTTP_400_BAD_REQUEST)

        txn = approval.transaction
        source_account = txn.account
        
        # Re-check balance (atomic helps here)
        if txn.transaction_type in [Transaction.TransactionType.WITHDRAWAL, Transaction.TransactionType.TRANSFER]:
             if source_account.balance < txn.amount:
                 approval.status = ApprovalRequest.ApprovalStatus.REJECTED
                 approval.reason = "Insufficient funds at approval time"
                 approval.decision_at = timezone.now()
                 approval.approved_by = request.user
                 approval.save()
                 txn.status = Transaction.TransactionStatus.FAILED
                 txn.save()
                 return Response({'error': 'Insufficient funds, request rejected'}, status=status.HTTP_400_BAD_REQUEST)

        # Execute
        if txn.transaction_type == Transaction.TransactionType.WITHDRAWAL:
            source_account.balance -= txn.amount
            source_account.save()
        elif txn.transaction_type == Transaction.TransactionType.TRANSFER:
            source_account.balance -= txn.amount
            source_account.save()
            if txn.destination_account:
                txn.destination_account.balance += txn.amount
                txn.destination_account.save()

        txn.status = Transaction.TransactionStatus.COMPLETED
        txn.save()

        approval.status = ApprovalRequest.ApprovalStatus.APPROVED
        approval.decision_at = timezone.now()
        approval.approved_by = request.user
        approval.save()

        AuditLog.objects.create(
            user=request.user,
            action=f"APPROVED_TRANSACTION_{txn.id}",
            details={'amount': str(txn.amount)}
        )

        return Response(ApprovalRequestSerializer(approval).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        approval = self.get_object()
        if approval.status != ApprovalRequest.ApprovalStatus.PENDING:
            return Response({'error': 'Request already processed'}, status=status.HTTP_400_BAD_REQUEST)

        approval.status = ApprovalRequest.ApprovalStatus.REJECTED
        approval.decision_at = timezone.now()
        approval.approved_by = request.user
        approval.reason = request.data.get('reason', 'Rejected by manager')
        approval.save()
        
        approval.transaction.status = Transaction.TransactionStatus.FAILED
        approval.transaction.save()

        AuditLog.objects.create(
            user=request.user,
            action=f"REJECTED_TRANSACTION_{approval.transaction.id}",
            details={'reason': approval.reason}
        )

        return Response(ApprovalRequestSerializer(approval).data)

