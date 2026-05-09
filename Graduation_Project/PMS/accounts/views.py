from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManger
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            permission_classes = [permissions.IsManger]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        user = request.user
        new_password = request.data.get('password')

        if not new_password:
            return Response({"error": "Enter the new password"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"message": "password changed successfully!"}, status=status.HTTP_200_OK)
