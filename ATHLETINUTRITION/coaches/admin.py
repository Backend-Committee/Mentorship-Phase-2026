from django.contrib import admin
from .models import CoachRequest, CoachFeedback, WorkoutPlan, WorkoutPlanEntry

admin.site.register(CoachRequest)
admin.site.register(CoachFeedback)
admin.site.register(WorkoutPlan)
admin.site.register(WorkoutPlanEntry)