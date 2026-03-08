from django.contrib import admin

from blog.models import BlogPost, Category

# Rawan 
# blogtask6

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date', 'category')
    search_fields = ('title', 'content')
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)