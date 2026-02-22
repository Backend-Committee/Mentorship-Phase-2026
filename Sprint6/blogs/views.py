from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from user.models import User

from . import forms
from .models import BlogPost, Comment, Follow


# Create your views here.
class FollowToggle(LoginRequiredMixin, View):
    def post(self, request):
        author_id = request.POST.get("author_id")
        author = User.objects.get(pk=author_id)
        follow, created = Follow.objects.get_or_create(user=request.user, author=author)
        if not created:
            follow.delete()
            return JsonResponse({"status": "unfollowed"})

        return JsonResponse({"status": "followed"})


class BlogsListView(ListView):
    model = BlogPost
    template_name = 'blogs/blog_list.html'
    context_object_name = 'blogs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            followed_author_ids = set(
                Follow.objects.filter(user=self.request.user)
                .values_list("author_id", flat=True)
            )
            context['followed_author_ids'] = followed_author_ids
        return context

    def get_queryset(self):
        return (
            BlogPost.objects
            .filter(is_public=True)
            .select_related('author')
            .prefetch_related('comments')
            .order_by('-created_at')
        )

class BlogEditView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'blogs/blog_edit.html'
    fields = ['title', 'content_md', 'comments_enabled', 'is_public']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.object.slug
        return context

    def get_success_url(self):
        return f'/blog/{self.object.slug}/'

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = "blogs/blog_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy('blog_list')

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = forms.BlogPostFrom
    template_name = 'blogs/blog_create.html'
    success_url = reverse_lazy('blog_list')

    def get_slug_from_title(self, title):
        from django.utils.text import slugify
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while BlogPost.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def form_valid(self, form):
        form.instance.slug = self.get_slug_from_title(form.cleaned_data['title'])
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogsDetailView(DetailView):
    model = BlogPost
    template_name = 'blogs/blog.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        comments = Comment.objects.filter(post=self.object)
        context = super().get_context_data(**kwargs)
        context['comments'] = comments
        context['comment_form'] = forms.CommentFrom()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        self.object = self.get_object()
        form = forms.CommentFrom(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = self.object
            comment.save()
            return redirect("blog_detail", slug=self.object.slug)
