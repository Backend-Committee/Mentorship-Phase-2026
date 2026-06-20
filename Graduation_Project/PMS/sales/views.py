from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer, InvoiceItemSerializer
from accounts import permissions as account_permissions
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from shifts.models import Shift


# Create your views here.

class InvoiceView(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        current_shift = Shift.objects.filter(is_closed=False).last()
        if not current_shift:
            raise ValidationError({'shift':"No shift is opened"})
        serializer.save(shift=current_shift)
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.shift.is_closed and request.user.role != 'Manager':
            raise ValidationError({'shift':"Shift is closed you must do return invoice"})
        if not instance.is_valid:
            raise ValidationError({'is_valid':"invoice is not valid"})
        if instance.type == 'Return':
            raise ValidationError({'type':"cant return a return invoice make a Sale invoice"})

        for item in instance.items.all():
            medicine = item.medicine
            medicine.stock_quantity += item.quantity
            medicine.save()
        if instance.payment_method == 'Debt':
            instance.customer.total_debt -= instance.total_price
            instance.customer.save()
        instance.is_valid = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



class InvoiceItemView(viewsets.ReadOnlyModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
    permission_classes = [permissions.IsAuthenticated]

