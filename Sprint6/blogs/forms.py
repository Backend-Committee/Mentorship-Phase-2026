from django import forms
from markdownx.widgets import MarkdownxWidget

from .models import BlogPost, Comment


class BlogPostFrom(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content_md', 'comments_enabled', 'is_public']
        widgets = {
                "content": MarkdownxWidget(),
            }

class CommentFrom(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['content']
        widgets = {
                "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write your comment..."
            })
        }
