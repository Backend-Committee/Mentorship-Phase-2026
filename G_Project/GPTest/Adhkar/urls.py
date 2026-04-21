from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

#LoginView is a built in view that handels the login
#LogoutView is a built in view that handels the logout
#UserCreationForm is a built in form that handels the registration

urlpatterns = [
   # path('',views.home,name='home'),
    path('', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('home2/',views.home2,name='home'),
    path('adhkarList/',AdhkarList.as_view(),name='adkar_list'),
    path('adkar/<int:pk>/',AdhkarDetail.as_view(),name='adhkar_detail'),
    path('create/',AdhkarCreate.as_view(),name='adhkar_create'),
    path('update/<int:pk>/',AdhkarUpdate.as_view(),name='adhkar_update'),
    path('delete/<int:pk>/',AdhkarDelete.as_view(),name='adhkar_delete'),
    path('morning/',views.morning,name='morning'),
    path('evening/',views.evening,name='evening'),
    path('sleep/',views.sleep,name='sleep'),
    path('complete/<int:adhkhar_id>/', views.CompleteAdhkarView.as_view(), name='complete_adhkar'),
    path('Profile/', views.profile_view, name='profile'),
    path('save-reminder/', views.save_reminder, name='save_reminder'),
]