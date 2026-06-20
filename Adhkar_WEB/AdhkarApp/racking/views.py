from .serializer import userprogress, NotificationSerializer
from rest_framework import generics, permissions, serializers
from rest_framework.generics import CreateAPIView
from .models import UserProgress, Notification
from .signals import update_user_system
from django.utils import timezone


class RecordAdhkarProgressView(CreateAPIView):
    serializer_class = userprogress
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        adhkar_obj = serializer.validated_data['adhkar']

        # التأكد إن المستخدم مخلصش نفس الذكر النهاردة
        already_done = UserProgress.objects.filter(
            user=user,
            adhkar=adhkar_obj,
            completed_at__date=timezone.now().date()
        ).exists()

        if already_done:
            raise serializers.ValidationError(
                "لقد قمت بإنهاء هذا الذكر اليوم بالفعل!"
            )

        points = adhkar_obj.points_value
        serializer.save(user=user, points_earned=points)


class NotificationListCreate(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)