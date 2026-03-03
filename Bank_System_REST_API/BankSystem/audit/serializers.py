from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ('user', 'action', 'ip_address', 'timestamp', 'details')

# Usually Audit logs are read-only
