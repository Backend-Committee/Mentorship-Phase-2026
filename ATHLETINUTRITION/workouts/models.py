from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    WORKOUT_TYPES = [
        ('strength', 'Strength'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility'),
        ('rest', 'Rest'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    workout_type = models.CharField(max_length=50, choices=WORKOUT_TYPES)
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout_type} on {self.date}"