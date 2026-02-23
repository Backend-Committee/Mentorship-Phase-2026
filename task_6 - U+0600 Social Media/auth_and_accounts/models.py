from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(blank=True, null=True)