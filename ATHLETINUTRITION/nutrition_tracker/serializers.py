from rest_framework import serializers
from .models import NutritionLog

class NutritionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionLog
        fields = ['id', 'date', 'food_name', 'quantity_grams', 'calories_per_100g', 'protein_per_100g', 'total_calories', 'total_protein', 'created_at']
        read_only_fields = ['total_calories', 'total_protein', 'created_at']