from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


# Create your views here.

class UserLogin(LoginView):
    template_name = 'users/Login.html'
    next_page = 'index'

class UserLogout(LogoutView):
    next_page = 'login'

class UserSignup(CreateView):
    form_class = UserCreationForm
    template_name = 'users/Signup.html'
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)

        return response

