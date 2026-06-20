from rest_framework import serializers
from .models import Workout

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'date', 'workout_type', 'duration_minutes', 'notes', 'created_at']
        read_only_fields = ['created_at']