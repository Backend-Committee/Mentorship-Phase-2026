from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *
urlpatterns = [
    path('reward/',ListCreateReward.as_view()),
    path('reward/<int:pk>/',GetUpdateDeleteReward.as_view()),
    path('userprofile/',UserProfileView.as_view()),
    path('MyReward/',UserRewardList.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)