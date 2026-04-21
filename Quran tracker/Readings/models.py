from django.db import models
from rest_framework.fields import DecimalField

# from User.models import User
# from Room.models import Room
# Create your models here.

class Reading (models.Model):
    user = models.ForeignKey("User.User" , on_delete= models.CASCADE)
    room = models.ForeignKey("Room.Room" , on_delete= models.SET_NULL, null=True)
    room_name = models.CharField(max_length= 255)
    reading_date_time = models.DateTimeField()
    reading_amount = models.DecimalField(max_digits=4,decimal_places=2)
    fine_amount = models.DecimalField(max_digits= 5, decimal_places= 2)
    updated_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        if self.room and not self.room_name:
            self.room_name = self.room.name
        super().save(*args , **kwargs)
