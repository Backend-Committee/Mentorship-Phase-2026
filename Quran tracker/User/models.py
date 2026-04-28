from django.db import models
# from Room.models import Room
# Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
#
#     def __str__(self):
#         return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

class UserRoom(models.Model):
    user = models.ForeignKey("User.User" , on_delete= models.CASCADE)
    room = models.ForeignKey("Room.Room" , on_delete= models.SET_NULL, null=True)
    total_fine = models.DecimalField(max_digits= 10 , decimal_places= 2)
