from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import NutritionLog

class NutritionListView(LoginRequiredMixin, generic.ListView):
    model = NutritionLog
    template_name = 'nutrition_tracker/nutrition_list.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return NutritionLog.objects.filter(user=self.request.user).order_by('-date')
    

class NutritionCreateView(LoginRequiredMixin, generic.CreateView):
    model = NutritionLog
    template_name = 'nutrition_tracker/nutrition_form.html'
    fields = ['date', 'food_name', 'quantity_grams', 'calories_per_100g', 'protein_per_100g']
    success_url = reverse_lazy('nutrition_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NutritionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = NutritionLog
    template_name = 'nutrition_tracker/nutrition_form.html'
    fields = ['date', 'food_name', 'quantity_grams', 'calories_per_100g', 'protein_per_100g']
    success_url = reverse_lazy('nutrition_list')

class NutritionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = NutritionLog
    template_name = 'nutrition_tracker/nutrition_confirm_delete.html'
    success_url = reverse_lazy('nutrition_list')