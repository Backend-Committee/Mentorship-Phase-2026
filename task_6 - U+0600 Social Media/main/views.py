from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.utils.timezone import activate as activate_time_zone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .utils import is_owner

class PostList(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 5
    
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['is_owner'] = is_owner(self.request.user, self.object)

        return context
    

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name_suffix = "_create_form"
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        request.user
        return super().post(request, *args, **kwargs)
    
class PostUpdate(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name_suffix = "_update_form"
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    # Thought: 
    # in overridden dispatch method -> "self.object = self.get_object()"
    # this hits the database for the object twice, the first one
    # is in dispatch method, and the second one internally in the post method
    # but how can I solve this ?
    # i got a solution in PostDelete but I am not sure if this is a safe way.
    
    def test_func(self):
        return is_owner(self.request.user, self.object)
    

class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    success_url  = reverse_lazy("post_list")
    
    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        return super().get_object(queryset)
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def test_func(self):
        return is_owner(self.request.user, self.object)

      
@login_required
def home(request):
    return render(request, "main/home.html")
