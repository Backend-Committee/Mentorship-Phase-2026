from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from .models import Shift, Expense
from .serializers import ShiftSerializer, ExpenseSerializer
from accounts import permissions
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.response import Response


# Create your views here.

class ShiftView(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

    def get_permissions(self):
        if self.action in ['list', 'destroy']:
            permission_classes = [permissions.IsManger]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        active_shift = Shift.objects.filter(is_closed=False).first()
        if active_shift:
            raise ValidationError({"detail": "there is already an active shift"})

        shift = serializer.save()
        shift.user.add(self.request.user)

    @action(detail=True, methods=['post'])
    def close_shift(self, request, pk=None):
        shift = self.get_object()

        if shift.is_closed:
            raise ValidationError({"detail": "the shift is already closed"})

        closing_cash = request.data.get('closing_cash')
        if closing_cash is None:
            raise ValidationError({"closing_cash": "Enter the closing cash first"})

        try:
            closing_cash = float(closing_cash)
        except ValueError:
            raise ValidationError({"closing_cash": "the closing cash must be an integer"})

        shift.closing_cash = closing_cash
        shift.end_time = timezone.now()
        shift.is_closed = True
        shift.save()

        serializer = self.get_serializer(shift)
        return Response({
            "detail": "the shift has been closed successfully",
            "shift_summary": serializer.data}, status=status.HTTP_200_OK)

class ExpenseView(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-created_at')
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        active_shift = Shift.objects.filter(is_closed=False).first()
        if not active_shift:
            raise ValidationError({"detail": "No open shift found to add expense."})
        serializer.save(shift=active_shift)
