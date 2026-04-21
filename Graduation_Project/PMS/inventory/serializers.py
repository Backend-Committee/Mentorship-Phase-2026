from rest_framework import serializers
from .models import Medicine, Shortage

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price cannot be negative')
        return value
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock cannot be negative')
    def validate_min_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Minimum stock cannot be negative')
        return value

class ShortageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shortage
        fields = '__all__'

    def create(self, validated_data):
        medicine = validated_data.get('medicine')
        if medicine:
            validated_data['medicine_name'] = medicine.name
        elif not validated_data.get('medicine_name'):
            raise serializers.ValidationError({'medicine_name':'Medicine name cannot be empty'})
        return super().create(validated_data)
