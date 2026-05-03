from django.urls import path
from .views import LogReadingView

urlpatterns = [
    path('<int:room_id>/readings/', LogReadingView.as_view(), name='log-reading'),
]