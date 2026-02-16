from django.db import models

# Create your models here.
# Basically, models are the base of database, and they are used to create the tables in the database. Each model is a class that inherits from models.Model, and each attribute of the class is a field in the table. For example, if we want to create a table for blog posts, we can create a model like this:
# and then make the tables, we can derive smaller tabels from the class

# $ python manage.py makemigrations blogs


# $ python manage.py sqlmigrate blogs 0001
# this command will show the SQL code that will be executed when we run the migrate command.
# We can use this command to check if our models are correct before we run the migrate command.
# After we run the migrate command, the tables will be created in the database, and we can start using them to store data.


from django.db import models
from django.utils import timezone
from django.utils.text import slugify
# the slug is the part of the url that identifies a particular page on a website in a form readable by users.
# It is usually the title of the page, but it can be anything that is unique and descriptive.
# For example, if we have a blog post with the title "My First Blog Post", the slug could be "my-first-blog-post".
# We can use the slug to create a URL for the blog post, such as "www.example.com/blog/my-first-blog-post".
# The slug is usually generated automatically from the title of the page, but it can also be manually specified.
# In Django, we can use the slugify function to generate a slug from a string.

# category of blog posts
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    # what are the kwargs in the save method?
    # The kwargs in the save method are used to pass additional arguments to the save method.
    # For example, if we want to update only a specific field in the database, we can use the update_fields argument to specify which fields to update.
    # This can be useful for performance reasons, as it will only update the specified fields instead of updating all fields in the database.
    # In the increment_views method, we use the update_fields argument to specify that we only want to update the views_count field in the database when we increment the view count.
    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    # """Blog post model"""
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    published_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


# """Comment model for blog posts"""
class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'