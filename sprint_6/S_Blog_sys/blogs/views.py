from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'blogs/List.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blogs/Details.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blogs/Create.html'
    fields = ['title','content']
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blogs/Update.html'
    fields = ['title','content']
    success_url = reverse_lazy('list')

    def test_func(self):
        if self.request.user == self.get_object().user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blogs/Delete.html'
    success_url = reverse_lazy('list')

    def test_func(self):
        if self.request.user == self.get_object().user:
            return Trun
        return False





