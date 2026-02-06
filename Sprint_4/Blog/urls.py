from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('Poets.html',views.poets, name = 'poets'),
]