from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from workouts.models import Workout
from nutrition_tracker.models import NutritionLog
from django.db.models import Sum
from coaches.models import CoachFeedback, WorkoutPlan

class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())

        context['weekly_workouts'] = Workout.objects.filter(
            user=self.request.user, date__gte=week_start).count()
        context['weekly_minutes'] = Workout.objects.filter(
            user=self.request.user, date__gte=week_start).aggregate(
            Sum('duration_minutes'))['duration_minutes__sum'] or 0
        context['today_calories'] = NutritionLog.objects.filter(
            user=self.request.user, date=today).aggregate(
            Sum('total_calories'))['total_calories__sum'] or 0
        context['today_protein'] = NutritionLog.objects.filter(
            user=self.request.user, date=today).aggregate(
            Sum('total_protein'))['total_protein__sum'] or 0
        context['recent_workouts'] = Workout.objects.filter(
            user=self.request.user).order_by('-date')[:5]
        context['coach_feedback'] = CoachFeedback.objects.filter(
        workout__user=self.request.user).order_by('-created_at')
        context['workout_plans'] = WorkoutPlan.objects.filter(
        athlete__user=self.request.user).order_by('-week_start_date')
        return context
