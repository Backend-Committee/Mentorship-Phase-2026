from rest_framework import serializers

from .models import AnalysisResult


class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = (
            'id',
            'extraction_task',
            'source_text',
            'parsed_metrics',
            'analyzed_at',
        )
        read_only_fields = ('id', 'parsed_metrics', 'analyzed_at')


class AnalysisCreateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AnalysisResult
        fields = ('extraction_task', 'text')

    def create(self, validated_data):
        text = validated_data.pop('text')
        validated_data['source_text'] = text
        return validated_data
