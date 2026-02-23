from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_start_of_content(self):
        if len(self.content) > 256:
            return self.content[:256] + "..."
        return self.content
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    