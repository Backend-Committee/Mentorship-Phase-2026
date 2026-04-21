from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=11)
    role = models.CharField(max_length=10, choices=[('Manager','Manager'),('Pharmacist','Pharmacist')],default='Pharmacist')
    hourly_rate = models.DecimalField(max_digits=5,decimal_places= 2,default=0)
    worked_hours = models.DecimalField(max_digits=5,decimal_places= 2,default=0)

    def __str__(self):
        return self.username


