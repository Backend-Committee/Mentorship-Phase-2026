from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=250)

    def __str__(self):
        return self.name
