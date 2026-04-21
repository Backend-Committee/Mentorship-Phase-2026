from django.db import models
from django.contrib.auth.models import User 


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Adhkar(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='adhkars', null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    points_value = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100,default="User")
    email=models.EmailField(default="test@example.com")
    password=models.CharField(max_length=100,default="password")
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    is_enabled = models.BooleanField(default=True)
    reminder_time = models.TimeField()


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adhkar = models.ForeignKey(Adhkar, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    points_earned = models.IntegerField()
    


class Reward(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    points_threshold = models.IntegerField()
    photo=models.ImageField(upload_to='rewards/', null=True, blank=True)
    reward_type = models.CharField(max_length=50) 

    def __str__(self):
        return self.title


class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)