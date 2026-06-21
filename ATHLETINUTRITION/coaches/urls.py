from django.urls import path
from . import views

urlpatterns = [
    path('', views.CoachListView.as_view(), name='coach_list'),
    path('request/<int:coach_id>/', views.SendCoachRequestView.as_view(), name='send_request'),
    path('requests/', views.CoachRequestListView.as_view(), name='coach_requests'),
    path('requests/accept/<int:pk>/', views.AcceptRequestView.as_view(), name='accept_request'),
    path('requests/decline/<int:pk>/', views.DeclineRequestView.as_view(), name='decline_request'),
    path('athlete/<int:pk>/', views.AthleteDetailView.as_view(), name='athlete_detail'),
    path('feedback/<int:workout_id>/', views.AddFeedbackView.as_view(), name='add_feedback'),
    path('plan/create/', views.WorkoutPlanCreateView.as_view(), name='plan_create'),
    path('leave/', views.LeaveCoachView.as_view(), name='leave_coach'),
    path('my-athletes/', views.MyAthletesView.as_view(), name='my_athletes'),
]