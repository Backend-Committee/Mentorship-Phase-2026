from rest_framework import serializers
from .models import Reading

class LogReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Reading
        fields = [
            'id',
            'user',
            'room',
            'room_name',
            'reading_date_time',
            'reading_amount',
            'fine_amount',
            'updated_at'
        ]
        read_only_fields = [
            'user',
            'room',
            'room_name',
            'reading_date_time',
            'fine_amount',
            'updated_at'
        ]

    def validate_reading_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Reading amount must be a positive value and greater than or equal to 1"
            )
        return value