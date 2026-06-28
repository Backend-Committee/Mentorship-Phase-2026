from rest_framework import viewsets, status, permissions
from rest_framework.exceptions import ValidationError
from .models import Shift, Expense
from .serializers import ShiftSerializer, ExpenseSerializer
from accounts import permissions as account_permissions
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.response import Response
from decimal import Decimal, InvalidOperation


# Create your views here.

class ShiftView(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

    def get_permissions(self):
        if self.action in ['list', 'destroy']:
            permission_classes = [account_permissions.IsManger]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        active_shift = Shift.objects.filter(is_closed=False).first()
        if active_shift:
            raise ValidationError({"detail": "there is already an active shift"})

        shift = serializer.save()
        shift.user.add(self.request.user)

    @action(detail=False, methods=['post'])
    def close_shift(self, request):
        shift = Shift.objects.filter(is_closed=False).first()

        if not shift:
            raise ValidationError({"detail": "there is no shift opened"})

        closing_cash = request.data.get('closing_cash')
        if closing_cash is None:
            raise ValidationError({"closing_cash": "Enter the closing cash first"})

        try:
            closing_cash = Decimal(str(closing_cash))
        except (ValueError, InvalidOperation):
            raise ValidationError({"closing_cash": "the closing cash must be a valid number"})

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
