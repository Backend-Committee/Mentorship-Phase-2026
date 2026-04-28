from rest_framework import serializers
from .models import Customer, BankAccount, Transaction

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Customer
        fields = '__all__'

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BankAccount
        fields = '__all__'

    def validate_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("Balance cannot be negative.")
        return value


class DepositWithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class TransferSerializer(serializers.Serializer):
    to_account_id = serializers.IntegerField()
    amount        = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Transaction
        fields = '__all__'