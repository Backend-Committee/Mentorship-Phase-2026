from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar_url = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    avg_rating = models.FloatField(default=0.0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.EmailField(unique=True)