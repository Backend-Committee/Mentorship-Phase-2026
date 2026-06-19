from django.db import models
from django.contrib.auth.models import User


class NutritionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    food_name = models.CharField(max_length=200)
    quantity_grams = models.FloatField()
    calories_per_100g = models.FloatField()
    protein_per_100g = models.FloatField()
    total_calories = models.FloatField(editable=False)
    total_protein = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_calories = (self.quantity_grams / 100) * self.calories_per_100g
        self.total_protein = (self.quantity_grams / 100) * self.protein_per_100g
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.food_name} on {self.date}"