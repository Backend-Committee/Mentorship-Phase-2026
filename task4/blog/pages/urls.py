from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('blogList',views.blogList,name='blogList'),
    path('blogDetails',views.blogDetails,name='blogDetails'),
]