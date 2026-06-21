from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    ACTIVITY_LEVEL_CHOICES = (
        ('sedentary', 'Sedentary'),
        ('light', 'Light Exercise'),
        ('moderate', 'Moderate Exercise'),
        ('active', 'Very Active'),
        ('very_active', 'Extra Active'),
    )

    GOAL_CHOICES = (
        ('lose_weight', 'Lose Weight'),
        ('maintain', 'Maintain'),
        ('gain_muscle', 'Gain Muscle'),
        ('improve_fitness', 'Improve Fitness'),
    )

    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, null=True, blank=True)
    activity_level = models.CharField(max_length=15, choices=ACTIVITY_LEVEL_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
