from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Doctor, LabAdmin
from .serializers import (DoctorSerializer, LabAdminSerializer,
                          UserCreateSerializer, UserSerializer)

User = get_user_model()


class UserListView(generics.ListAPIView):
    """List all users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveAPIView):
    """Retrieve a single user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserCreateView(generics.CreateAPIView):
    """Create a new user."""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class CurrentUserView(APIView):
    """Get the currently authenticated user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class DoctorListView(generics.ListCreateAPIView):
    """List all doctors or create a new doctor profile."""

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAdminUser]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a doctor profile."""

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class LabAdminListView(generics.ListCreateAPIView):
    """List all lab admins or create a new lab admin profile."""

    queryset = LabAdmin.objects.all()
    serializer_class = LabAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class LabAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a lab admin profile."""

    queryset = LabAdmin.objects.all()
    serializer_class = LabAdminSerializer
    permission_classes = [permissions.IsAdminUser]
