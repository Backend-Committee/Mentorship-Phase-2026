from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import blog, Profile
from .forms import RegisterForm


class RegisterView(View):
    template_name = "registration/register.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(
                request, f"Account created for {user.username}! You can now login."
            )
            return redirect("login")  # الأفضل توديه للوجن بعد التسجيل
        return render(request, self.template_name, {"form": form})


class PostListView(ListView):
    model = blog
    template_name = "pages/blogs_list.html"
    context_object_name = "blogs"
    ordering = ["-id"]  # عشان أحدث البوستات تظهر فوق


class PostDetailView(DetailView):
    model = blog
    template_name = "pages/detail.html"
    context_object_name = "blog"


class createView(LoginRequiredMixin, CreateView):
    model = blog
    fields = ["title", "content", "category", "image"]
    template_name = "pages/blog_form.html"
    success_url = reverse_lazy("blogs")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = blog
    fields = ["title", "content", "category", "image"]
    template_name = "pages/blog_form.html"
    success_url = reverse_lazy("blogs")

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = blog
    template_name = "pages/blog_confirm_delete.html"
    success_url = reverse_lazy("blogs")

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author