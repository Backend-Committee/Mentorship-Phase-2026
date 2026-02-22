from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import BlogPost, Comment, Follow

# Register your models here.
@admin.register(BlogPost)
class PostAdmin(MarkdownxModelAdmin):
    pass
admin.site.register(Comment)
admin.site.register(Follow)
