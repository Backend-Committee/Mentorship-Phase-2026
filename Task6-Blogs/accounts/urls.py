from django.urls import include, path

urlpatterns = [
    path('login/', include('django.contrib.auth.urls')),
    path('logout/', include('django.contrib.auth.urls')),
    path('register/', include('accounts.urls')),
    
]
