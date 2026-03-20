from rest_framework import viewsets, status, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from .serializers import UserSerializer, UserRegistrationSerializer
from .permissions import IsOwnerOrAdmin
from audit.models import AuditLog


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action == 'list':
             # Admin/Manager check is in list() override
             return [permissions.IsAuthenticated()]
        # For object actions (retrieve, update, destroy)
        return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]

    def list(self, request, *args, **kwargs):
        # Restrict listing users to Admin/Manager
        if request.user.role not in [User.Role.ADMIN, User.Role.MANAGER]:
             return Response(status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Log registration?
        return response

