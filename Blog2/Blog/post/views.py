from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Comment, Like, Poll, PollOption, PollVote, PollComment
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django import forms

class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            # Search in title and rich text body
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(body__icontains=query)
            ).distinct()
        return queryset

class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['likes_count'] = post.likes.count()
        if self.request.user.is_authenticated:
            context['liked'] = post.likes.filter(user=self.request.user).exists()
        else:
            context['liked'] = False
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'body', 'image']
    template_name = 'post/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'body', 'image']
    template_name = 'post/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        body = request.POST.get('body')
        if body:
            Comment.objects.create(post=post, author=request.user, body=body)
        return redirect('post-detail', pk=pk)

class AddLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()  # Toggle like
        return redirect('post-detail', pk=pk)

# Poll Views

class PollListView(ListView):
    model = Poll
    template_name = 'post/poll_list.html'
    context_object_name = 'polls'
    ordering = ['-created_at']

class PollCreateView(LoginRequiredMixin, CreateView):
    model = Poll
    fields = ['question', 'active']
    template_name = 'post/poll_form.html'
    success_url = reverse_lazy('poll-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        # Handle options
        options = self.request.POST.getlist('options')
        for option_text in options:
            if option_text.strip():
                PollOption.objects.create(poll=self.object, text=option_text)
        return response

class PollDetailView(DetailView):
    model = Poll
    template_name = 'post/poll_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_voted'] = PollVote.objects.filter(poll=self.object, user=self.request.user).exists()
        else:
            context['user_voted'] = False
        return context

class PollVoteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=pk)
        option_id = request.POST.get('option')
        if not option_id:
             return redirect('poll-detail', pk=pk)
             
        option = get_object_or_404(PollOption, pk=option_id)
        
        # Check if already voted
        if PollVote.objects.filter(poll=poll, user=request.user).exists():
            return HttpResponseForbidden("You have already voted.")

        PollVote.objects.create(poll=poll, user=request.user, option=option)
        return redirect('poll-detail', pk=pk)

class PollCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=pk)
        body = request.POST.get('body')
        if body:
            PollComment.objects.create(poll=poll, author=request.user, body=body)
        return redirect('poll-detail', pk=pk)

