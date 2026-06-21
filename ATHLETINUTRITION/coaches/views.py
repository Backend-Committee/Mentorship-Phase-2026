from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import CoachRequest, CoachFeedback, WorkoutPlan, WorkoutPlanEntry
from users.models import CoachProfile, AthleteProfile
from workouts.models import Workout


class SendCoachRequestView(LoginRequiredMixin, generic.View):
    def post(self, request, coach_id):
        coach = get_object_or_404(CoachProfile, id=coach_id)
        athlete = get_object_or_404(AthleteProfile, user=request.user)
        CoachRequest.objects.get_or_create(athlete=athlete, coach=coach, defaults={'status': 'pending'})
        return redirect('coach_list')
   

class CoachListView(LoginRequiredMixin, generic.ListView):
    model = CoachProfile
    template_name = 'coaches/coach_list.html'
    context_object_name = 'coaches'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            athlete_profile = AthleteProfile.objects.get(user=self.request.user)
            context['athlete_profile'] = athlete_profile
            context['pending_requests'] = CoachRequest.objects.filter(
                athlete=athlete_profile, status='pending')
        except AthleteProfile.DoesNotExist:
            context['athlete_profile'] = None
            context['pending_requests'] = []
        return context

class AcceptRequestView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        coach_request = get_object_or_404(CoachRequest, pk=pk)
        coach_request.status = 'accepted'
        coach_request.save()
        coach_request.athlete.coach = coach_request.coach
        coach_request.athlete.save()
        return redirect('coach_requests')

class DeclineRequestView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        coach_request = get_object_or_404(CoachRequest, pk=pk)
        coach_request.status = 'declined'
        coach_request.save()
        return redirect('coach_requests')



class CoachRequestListView(LoginRequiredMixin, generic.ListView):
    model = CoachRequest
    template_name = 'coaches/coach_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        coach = get_object_or_404(CoachProfile, user=self.request.user)
        return CoachRequest.objects.filter(coach=coach, status='pending')
    
class AthleteDetailView(LoginRequiredMixin, generic.DetailView):
    model = AthleteProfile
    template_name = 'coaches/athlete_detail.html'
    context_object_name = 'athlete'

class AddFeedbackView(LoginRequiredMixin, generic.CreateView):
    model = CoachFeedback
    template_name = 'coaches/feedback_form.html'
    fields = ['feedback_text']
    success_url = reverse_lazy('workout_list')

    def form_valid(self, form):
        form.instance.coach = get_object_or_404(CoachProfile, user=self.request.user)
        form.instance.workout = get_object_or_404(Workout, pk=self.kwargs['workout_id'])
        return super().form_valid(form)

class WorkoutPlanCreateView(LoginRequiredMixin, generic.CreateView):
    model = WorkoutPlan
    template_name = 'coaches/plan_form.html'
    fields = ['athlete', 'week_start_date', 'title', 'notes']
    success_url = reverse_lazy('coach_requests')

    def form_valid(self, form):
        form.instance.coach = get_object_or_404(CoachProfile, user=self.request.user)
        return super().form_valid(form)
    
class LeaveCoachView(LoginRequiredMixin, generic.View):
    def post(self, request):
        athlete = get_object_or_404(AthleteProfile, user=request.user)
        athlete.coach = None
        athlete.save()
        return redirect('coach_list')
    
class MyAthletesView(LoginRequiredMixin, generic.ListView):
    model = AthleteProfile
    template_name = 'coaches/my_athletes.html'
    context_object_name = 'athletes'

    def get_queryset(self):
        coach = get_object_or_404(CoachProfile, user=self.request.user)
        return AthleteProfile.objects.filter(coach=coach)