from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import viewsets
from .models import Customer, CustomerDebts, DebtPayment
from shifts.models import Shift
from .serializers import CustomerSerializer, CustomerDebtsSerializer, DebtPaymentSerializer
from ..accounts import permissions


# Create your views here.

class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-total_debt')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'Manager':
            raise PermissionDenied("You are not allowed to delete customers")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role != 'Manager' and request.data.get('total_debt') :
            raise PermissionDenied("You are not allowed to edit customers debt")
        return super().update(request, *args, **kwargs)

class CustomerDebtsView(viewsets.ModelViewSet):
    queryset = CustomerDebts.objects.all()
    serializer_class = CustomerDebtsSerializer
    permission_classes = [permissions.IsAuthenticated]
    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'Manager':
            raise PermissionDenied("You are not allowed to delete customers debt")
        return super().destroy(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        if request.user.role != 'Manager':
            raise PermissionDenied("You are not allowed to edit customers debt")
        return super().update(request, *args, **kwargs)

class DebtPaymentView(viewsets.ModelViewSet):
    queryset = DebtPayment.objects.all().order_by('-payment_date')
    serializer_class = DebtPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        current_shift = Shift.objects.filter(is_closed = False).last()
        if not current_shift:
            raise ValidationError({'shift': "No shift is opened"})

        serializer.save(shift = current_shift)
