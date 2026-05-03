from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(
        "User.User",
        related_name='admin_rooms',
        on_delete=models.SET_NULL,
        null=True,
    )
    reading_deadline = models.TimeField()
    daily_fine = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name