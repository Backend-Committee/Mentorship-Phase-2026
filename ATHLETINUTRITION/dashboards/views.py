from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/dashboard.html'