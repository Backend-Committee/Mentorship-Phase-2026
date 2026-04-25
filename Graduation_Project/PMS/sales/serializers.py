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
            if q > med.quantity:
                raise serializers.ValidationError({'quantity', "Quantity cannot be greater than medicine."})
        return data


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['total_price', 'shift', 'is_valid', 'created_at']

    def validate(self, data):
        items = data.get('items', [])
        if not items:
            raise serializers.ValidationError({'items': "cant be empty"})
        return data

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_price = sum(item[quantity] * item[unit_price] for item in items_data)
        invoice = Invoice.objects.create(total_price=total_price, **validated_data)

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
