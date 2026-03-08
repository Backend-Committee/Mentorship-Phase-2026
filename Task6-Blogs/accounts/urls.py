from django.urls import include, path
from accounts import views

# extremly important if we need to use the url in our template
app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_user.as_view() , name='login'),
    path('logout/', views.logout_user.as_view(), name='logout'),
    path('register/', views.register_user.as_view(), name='register'),
    
]
