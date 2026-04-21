from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('MISSED_DAY', 'Missed Day'),
        ('FINE_APPLIED', 'Fine Applied'),
        ('ROOM_INVITE', 'Room Invite'),
        ('GENERAL', 'General'),
    )
    user = models.ForeignKey("User.User" , on_delete= models.CASCADE)
    room = models.ForeignKey("Room.Room" , on_delete= models.SET_NULL , null=True, blank=True)
    message = models.CharField(max_length= 255)
    type = models.CharField(max_length= 255, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
