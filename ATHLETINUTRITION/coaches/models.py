from django.db import models
from users.models import CoachProfile, AthleteProfile
from workouts.models import Workout

class CoachRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    athlete = models.ForeignKey(AthleteProfile, on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.athlete} -> {self.coach} ({self.status})"

class CoachFeedback(models.Model):
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.coach} on {self.workout}"

class WorkoutPlan(models.Model):
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    athlete = models.ForeignKey(AthleteProfile, on_delete=models.CASCADE)
    week_start_date = models.DateField()
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.athlete}"

class WorkoutPlanEntry(models.Model):
    DAYS = [
        ('monday', 'Monday'), ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'), ('thursday', 'Thursday'),
        ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday'),
    ]
    WORKOUT_TYPES = [
        ('strength', 'Strength'), ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility'), ('rest', 'Rest'),
    ]
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20, choices=DAYS)
    workout_type = models.CharField(max_length=50, choices=WORKOUT_TYPES)
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.plan.title} - {self.day_of_week}"