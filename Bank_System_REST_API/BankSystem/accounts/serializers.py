from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_number', 'user', 'balance', 'is_frozen', 'created_at')
        read_only_fields = ('account_number', 'balance', 'created_at', 'user', 'is_frozen')
