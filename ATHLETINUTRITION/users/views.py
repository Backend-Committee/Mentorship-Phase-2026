from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AthleteProfile
from .forms import AthleteProfileForm


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class AthleteProfileView(LoginRequiredMixin, generic.UpdateView):
    model = AthleteProfile
    form_class = AthleteProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        profile, created = AthleteProfile.objects.get_or_create(user=self.request.user)
        return profile