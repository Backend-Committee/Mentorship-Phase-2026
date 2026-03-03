from rest_framework import viewsets, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer
from users.permissions import IsAuditor, IsAdmin, IsManager

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsManager | IsAuditor]

