from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import post
from .forms import PostForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    posts = post.objects.all().order_by('-created_at')
    return render(request, 'blogs/home.html', {'posts': posts})

def post_detail(request, pk):
    post_obj = get_object_or_404(post, pk=pk)
    return render(request, 'blogs/post_detail.html', {'post': post_obj})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blogs/create_post.html', {'form': form})

@login_required
def my_posts(request):
    posts = post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blogs/my_posts.html', {'posts': posts})




