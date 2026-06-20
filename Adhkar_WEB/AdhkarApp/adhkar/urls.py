from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *
urlpatterns = [
    path('adhkar/',ListCreateAdhkar.as_view()),
    path('adhkar/<int:pk>/',GetUpdateDeleteAdhkar.as_view()),
    path('categories/',ListCreateCategory.as_view()),
    path('categories/<int:pk>/',CategoryDetail.as_view()),
]