from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Reward(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    points_threshold = models.IntegerField()
    reward_type = models.CharField(max_length=50) 
    image = models.ImageField(upload_to='rewards_images/', null=True, blank=True)
    def __str__(self):
        return self.title

class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlocked_rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'reward') # لمنع تكرار نفس الجائزة لنفس المستخدم

