from django.urls import path
from BackEnd.Controller import bookController
from BackEnd.middlewares.auth_middlware import requireAuth



urlpatterns = [
    path('random', requireAuth(bookController.getRandomBook)),
    path('highest', requireAuth(bookController.getHighestBook)),
    path('oldest', requireAuth(bookController.getOldestBook)),
    path('favorite', requireAuth(bookController.addFavoriteBook)),
    path('favorites', requireAuth(bookController.getMyFavorites)),
]