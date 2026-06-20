from django.db import models
from django.contrib.auth.models import User

class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    specialty = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Coach: {self.user.username}"

class AthleteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachProfile, on_delete=models.SET_NULL, null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    height_cm = models.FloatField(null=True, blank=True)
    sport_type = models.CharField(max_length=100, blank=True)
    weekly_calorie_goal = models.FloatField(null=True, blank=True)
    weekly_protein_goal = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Athlete: {self.user.username}"