from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Workout
from rest_framework import viewsets, permissions
from .serializers import WorkoutSerializer


class WorkoutListView(LoginRequiredMixin, generic.ListView):
    model = Workout
    template_name = 'workouts/workout_list.html'
    context_object_name = 'workouts'

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).order_by('-date')

class WorkoutCreateView(LoginRequiredMixin, generic.CreateView):
    model = Workout
    template_name = 'workouts/workout_form.html'
    fields = ['date', 'workout_type', 'duration_minutes', 'notes']
    success_url = reverse_lazy('workout_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WorkoutUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Workout
    template_name = 'workouts/workout_form.html'
    fields = ['date', 'workout_type', 'duration_minutes', 'notes']
    success_url = reverse_lazy('workout_list')

class WorkoutDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Workout
    template_name = 'workouts/workout_confirm_delete.html'
    success_url = reverse_lazy('workout_list')



class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)