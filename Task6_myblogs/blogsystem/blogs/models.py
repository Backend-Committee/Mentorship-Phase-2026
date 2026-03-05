from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class blog(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="product_images/%y/%m/%d", blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category = models.CharField(
        max_length=30,
        choices=[
            ("Programming", "Programming"),
            ("Web Development", "Web Development"),
            ("AI", "Artificial Intelligence"),
            ("Tutorials", "Tutorials"),
            ("Personal", "Personal"),
        ],
        default="Personal",
    )
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
