from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.utils.timezone import activate as activate_time_zone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .utils import is_owner

CURRENT_TZ = "Africa/Cairo"

class PostList(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 5
    
    def get(self, request, *args, **kwargs):
        activate_time_zone(CURRENT_TZ)
        return super().get(request, *args, **kwargs)
    
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['is_owner'] = is_owner(self.request.user, self.object)

        return context
    
    def get(self, request, *args, **kwargs):
        activate_time_zone(CURRENT_TZ)
        return super().get(request, *args, **kwargs)

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name_suffix = "_create_form"
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class PostUpdate(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name_suffix = "_update_form"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def test_func(self):
        return is_owner(self.request.user, self.object)

class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    success_url  = reverse_lazy("post_list")
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def test_func(self):
        return is_owner(self.request.user, self.object)
    
    def get(self, request, *args, **kwargs):
        activate_time_zone(CURRENT_TZ)
        return super().get(request, *args, **kwargs)
      
@login_required
def home(request):
    return render(request, "main/home.html")
