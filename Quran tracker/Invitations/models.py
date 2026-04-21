from django.db import models
#rom Room.models import Room
# Create your models here.

class Invitation(models.Model):
     room = models.ForeignKey("Room.Room", on_delete=models.CASCADE)
     token = models.CharField(max_length=255 , unique=True)
     expires_at = models.DateTimeField()
     isUsed = models.BooleanField(default=False)

     def __str__(self):
         return f"Invitation for {self.room.name} - {self.token}"