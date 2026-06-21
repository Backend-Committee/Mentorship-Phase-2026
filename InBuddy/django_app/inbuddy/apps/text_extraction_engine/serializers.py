from rest_framework import serializers

from .models import ExtractionTask


class ExtractionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractionTask
        fields = (
            'id',
            'image',
            'extracted_text',
            'status',
            'error_message',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'extracted_text', 'status', 'error_message', 'created_at', 'updated_at')


class ExtractionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractionTask
        fields = ('image',)
