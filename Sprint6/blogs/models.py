from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Create your models here.
class BlogPost(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content_md = MarkdownxField()
    comments_enabled = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def formatted_markdown(self):
        return markdownify(self.content_md)

class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"

class Follow(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='following')
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'author')

    def __str__(self):
        return f"{self.user} starred {self.author}"
