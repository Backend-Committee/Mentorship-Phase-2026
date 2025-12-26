from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('BackEnd.routes.authRoutes')),
    
    path('api/books/', include('BackEnd.routes.bookRoutes')),
]