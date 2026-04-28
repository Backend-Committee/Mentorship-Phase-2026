from rest_framework import serializers
from .models import Shift, Expense
from django.db.models import Sum


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'shift')


class ShiftSerializer(serializers.ModelSerializer):
    total_sales = serializers.SerializerMethodField()
    total_expenses = serializers.SerializerMethodField()
    expected_cash = serializers.SerializerMethodField()
    difference = serializers.SerializerMethodField()
    expenses = ExpenseSerializer(many=True, read_only=True)

    class Meta:
        model = Shift
        fields = '__all__'
        read_only_fields = ('id', 'start_time', 'end_time', 'total_sales', 'total_expenses', 'expected_cash',
                            'difference', 'expenses')

    def get_total_sales(self, obj):
        total = obj.invoices.filter(is_valid=True).exclude(payment_method='Debt').aggregate(Sum('total_price'))[
            'total_price__sum']
        return total or 0

    def get_total_expenses(self, obj):
        total = obj.expenses.aggregate(Sum('amount'))['amount__sum']
        return total or 0

    def get_expected_cash(self, obj):
        sales = self.get_total_sales(obj)
        expenses = self.get_total_expenses(obj)
        return obj.starting_cash + sales - expenses

    def get_difference(self, obj):
        if not obj.is_closed:
            return 0.00
        return obj.closing_cash - self.get_expected_cash(obj)
