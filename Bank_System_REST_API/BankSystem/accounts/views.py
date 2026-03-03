from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer
from audit.models import AuditLog
from users.permissions import IsManager, IsAdmin

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == "CUSTOMER":
            return Account.objects.filter(user=user)
        return Account.objects.all()

    def perform_create(self, serializer):
        # Only Staff should create accounts properly, but for demo maybe allow authenticated users if needed?
        # Let's stricter it: Only admin creates for others, customer can create for self?
        # Usually checking permissions here
        serializer.save(user=self.request.user) # Assign to self by default if customer

    @action(detail=True, methods=['post'], permission_classes=[IsManager | IsAdmin])
    def freeze(self, request, pk=None):
        account = self.get_object()
        account.is_frozen = True
        account.save()
        
        AuditLog.objects.create(
            user=request.user,
            action=f"FROZE_ACCOUNT_{account.account_number}",
            details={'reason': request.data.get('reason', 'Admin action')}
        )
        return Response({'status': 'frozen'})

    @action(detail=True, methods=['post'], permission_classes=[IsManager | IsAdmin])
    def unfreeze(self, request, pk=None):
        account = self.get_object()
        account.is_frozen = False
        account.save()
        
        AuditLog.objects.create(
            user=request.user,
            action=f"UNFROZE_ACCOUNT_{account.account_number}",
            details={'reason': request.data.get('reason', 'Admin action')}
        )
        return Response({'status': 'active'})

