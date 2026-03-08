from django.http import HttpResponse
from django.db import models


from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import BlogPost, Category, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# understand everything in this page

# Home page view showing latest posts and statistics
# def home(request):
    # latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    # # Get statistics
    # total_posts = BlogPost.objects.filter(is_published=True).count()
    # total_categories = Category.objects.count()
    # total_comments = Comment.objects.count()
    
    # context = {
    #     'latest_posts': latest_posts,
    #     'total_posts': total_posts,
    #     'total_categories': total_categories,
    #     'total_comments': total_comments,
    # }
    # return render(request, 'home.html', context)
    
class HomeView(ListView):
    model = BlogPost
    template_name = 'home.html'
    context_object_name = 'latest_posts'
    queryset = BlogPost.objects.filter(is_published=True)[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = BlogPost.objects.filter(is_published=True).count()
        context['total_categories'] = Category.objects.count()
        context['total_comments'] = Comment.objects.count()
        return context

# Blog list view showing all published posts
# def blog_list(request):
#     posts = BlogPost.objects.filter(is_published=True).select_related('category')
    
#     context = {
#         'posts': posts,
#         'total_posts': posts.count(),
#     }
#     return render(request, 'blog_list.html', context)
class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog_list.html'
    context_object_name = 'posts'
    queryset = BlogPost.objects.filter(is_published=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = self.queryset.count()
        return context

# Blog detail view showing a single post with comments
# def blog_detail(request, slug):
#     post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
#     # Increment view count
#     post.increment_views()
    
#     comments = post.comments
    
#     context = {
#         'post': post,
#         'comments': comments,
#         'comment_count': comments.count(),
#     }
#     return render(request, 'blog_detail.html', context)

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_detail.html'
    context_object_name = 'post'

    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_count'] = self.object.comments.count()
        return context


# create a new blog, the createView handles the form automatically 
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog_form.html'
    fields = ['title', 'content', 'category', 'is_published']
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# update a blog post
class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    template_name = 'blog_form.html'
    fields = ['title', 'content', 'category', 'is_published']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # 403 if not author


# delete a blog post
# login mixin to require login, userpassestestmixin to check if the user is the author of the post, deleteview to handle the deletion of the post
class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  #  403 if not author

# View showing all categories with post counts
# def category_list(request):
#     categories = Category.objects.annotate(
#         post_count=Count('posts', filter=models.Q(posts__is_published=True))
#     )
    
#     context = {
#         'categories': categories,
#     }
#     return render(request, 'category_list.html', context)

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(
            post_count=Count('posts', filter=models.Q(posts__is_published=True))
        )

# View showing all posts in a specific category
# def category_posts(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     posts = BlogPost.objects.filter(
#         category=category, 
#         is_published=True
#     ).select_related('category')
    
#     context = {
#         'category': category,
#         'posts': posts,
#         'post_count': posts.count(),
#     }
#     return render(request, 'category_posts.html', context)
class CategoryPostsView(DetailView):
    model = Category
    template_name = 'category_posts.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = BlogPost.objects.filter(category=self.object, is_published=True)
        context['posts'] = posts
        context['post_count'] = posts.count()
        return context