from django.db import models
from accounts.models import User
from django.conf import settings
# Create your models here.

class Shift(models.Model):
    user_id = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shifts')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    starting_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    closing_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        status = "Closed" if self.is_closed else "Active"
        return f"Shift {self.id} ({status})"

class Expense(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.description}"