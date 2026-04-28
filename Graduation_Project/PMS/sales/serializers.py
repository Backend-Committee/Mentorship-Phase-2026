from django.db import transaction
from rest_framework import serializers
from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ['total_price']

    def validate(self, data):
        med = data.get('medicine')
        q = data.get('quantity')
        if med:
            if q > med.stock_quantity:
                raise serializers.ValidationError({'quantity': "Quantity cannot be greater than medicine."})
        return data


class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['total_price', 'shift', 'is_valid', 'created_at']

    def validate(self, data):
        items = data.get('items', [])
        if not items:
            raise serializers.ValidationError({'items': "cant be empty"})
        method = data.get('payment_method')
        customer = data.get('customer')
        if method == 'Debt' and not customer:
            raise serializers.ValidationError({'customer': "cant be empty while the invoice is Debt"})

        return data

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_price = sum(item['quantity'] * item['unit_price'] for item in items_data)
        invoice = Invoice.objects.create(total_price=total_price, **validated_data)

        if invoice.payment_method == 'Debt':
            invoice.customer.total_debt += invoice.total_price
            invoice.customer.save()


        for item in items_data:
            medicine = item['medicine']
            quantity = item['quantity']
            item_total = quantity * item['unit_price']
            InvoiceItem.objects.create(
                invoice=invoice,
                total_price=item_total,
                **item
            )
            medicine.stock_quantity -= quantity
            medicine.save()
        return invoice
