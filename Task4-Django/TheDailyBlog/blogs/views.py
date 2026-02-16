from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.db import models


from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import BlogPost, Category, Comment

# Home page view showing latest posts and statistics
def home(request):
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    # Get statistics
    total_posts = BlogPost.objects.filter(is_published=True).count()
    total_categories = Category.objects.count()
    total_comments = Comment.objects.filter(is_approved=True).count()
    
    context = {
        'latest_posts': latest_posts,
        'total_posts': total_posts,
        'total_categories': total_categories,
        'total_comments': total_comments,
    }
    return render(request, 'blog/home.html', context)

# Blog list view showing all published posts
def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).select_related('category')
    
    context = {
        'posts': posts,
        'total_posts': posts.count(),
    }
    return render(request, 'blog/blog_list.html', context)

# Blog detail view showing a single post with comments
def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count
    post.increment_views()
    
    # Get approved comments for this post
    comments = post.comments.filter(is_approved=True)
    
    context = {
        'post': post,
        'comments': comments,
        'comment_count': comments.count(),
    }
    return render(request, 'blog/blog_detail.html', context)

# View showing all categories with post counts
def category_list(request):
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=models.Q(posts__is_published=True))
    )
    
    context = {
        'categories': categories,
    }
    return render(request, 'blog/category_list.html', context)

# View showing all posts in a specific category
def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(
        category=category, 
        is_published=True
    ).select_related('category')
    
    context = {
        'category': category,
        'posts': posts,
        'post_count': posts.count(),
    }
    return render(request, 'blog/category_posts.html', context)