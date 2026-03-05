from rest_framework import serializers
from crud_app.models import Account
from .models import Transaction


# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ["id", "account", "to_account", "amount", "type", "created_at"]
#         read_only_fields = ["created_at"]


class DepositSerializer(serializers.Serializer):
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.select_related("customer").all()
    )
    amount = serializers.IntegerField(min_value=0)
    
    def validate_account(self, account):
        if account.customer is None or not account.active:
            raise serializers.ValidationError("this account is no longer active")
        return account

class WithdrawSerializer(serializers.Serializer):
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.select_related("account_type", "customer").all()
    )
    amount = serializers.IntegerField(min_value=0)
    
    def validate_account(self, account):
        if account.customer is None or not account.active:
            raise serializers.ValidationError("this account is no longer active")
        return account
    
    def validate(self, data):
        account = data['account']
        
        
        if data['amount'] > account.balance:
            raise serializers.ValidationError("you don't have enough balance to complete this operation")
        
        # TODO: ENFORCE MAXIMUM DAILY AND MONTHLY WITHDRAWAL LIMITS
        
        return data