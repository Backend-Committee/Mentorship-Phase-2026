from rest_framework import serializers
from .models import Reading
from datetime import date

class LogReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Reading
        fields = ['id', 'reading_amount', 'fine_amount', 'reading_date_time', 'room_name']
        read_only_fields = ['reading_date_time', 'room_name', 'fine_amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive value")
        return value