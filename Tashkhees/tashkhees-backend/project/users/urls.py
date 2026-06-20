from django.urls import path

from .views import (CurrentUserView, DoctorDetailView, DoctorListView,
                    LabAdminDetailView, LabAdminListView, UserCreateView,
                    UserDetailView, UserListView)

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("register/", UserCreateView.as_view(), name="user-create"),
    path("me/", CurrentUserView.as_view(), name="user-me"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),
    path("lab-admins/", LabAdminListView.as_view(), name="labadmin-list"),
    path("lab-admins/<int:pk>/", LabAdminDetailView.as_view(), name="labadmin-detail"),
]
