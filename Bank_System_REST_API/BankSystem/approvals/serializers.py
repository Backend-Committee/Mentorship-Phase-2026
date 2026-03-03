from rest_framework import serializers
from .models import ApprovalRequest

class ApprovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = '__all__'
        read_only_fields = ('requested_by', 'requested_at', 'status', 'decision_at', 'approved_by')
