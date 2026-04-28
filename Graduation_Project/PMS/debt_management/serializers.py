from django.db import transaction
from rest_framework import serializers
from .models import Customer, CustomerDebts, DebtPayment


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('id', 'total_debt')

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError({'phone': 'Phone number must be digits!'})
        elif value.len() != 11:
            raise serializers.ValidationError({'phone': 'Phone number must be 11!'})
        elif value.startswith('011', '012', '015', '010'):
            raise serializers.ValidationError({'phone': 'not an Egyptian phone number!'})
        return value


class CustomerDebtsSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = CustomerDebts
        fields = '__all__'


class DebtPaymentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = DebtPayment
        fields = '__all__'
        read_only_fields = ('id', 'payment_date', 'customer_name', 'shift')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError({'amount': 'Amount must be positive!'})
        return value

    def validate(self, data):
        amount = data.get('amount')
        customer = data.get('customer')

        if amount > customer.total_debt:
            raise serializers.ValidationError({'amount': 'Amount must be less than or equal to the total debt!'})
        return data

    @transaction.atomic
    def create(self, validated_data):
        payment = super().create(validated_data)
        customer = payment.customer
        customer.total_debt -= payment.amount
        customer.save()
        return payment


