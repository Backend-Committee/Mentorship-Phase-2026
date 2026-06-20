from rest_framework import viewsets, permissions, filters, status
from .models import  Medicine, Shortage
from .serializers import MedicineSerializer, ShortageSerializer
from rest_framework.exceptions import PermissionDenied, ValidationError
from accounts import permissions as custom_permissions
from rest_framework.decorators import action
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class MedicineView(viewsets.ModelViewSet):
    queryset = Medicine.objects.all().order_by('name')
    serializer_class = MedicineSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'barcode']
    filterset_fields = ['type']

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'Manager':
            raise PermissionDenied("Manger Only can delete Medicine")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_stock = request.data.get('stock_quantity')
        if request.user.role != 'Manager' and new_stock is not None:
            if int(new_stock) < instance.stock_quantity:
                raise ValidationError({"stock_quantity": "Stock quantity can't be decreased manually"})
        return super().update(request, *args, **kwargs)


    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_medicines = self.get_queryset().filter(stock_quantity__lte=F('min_stock'))
        serializer = self.get_serializer(low_stock_medicines, many=True)
        return Response(serializer.data)


class ShortageView(viewsets.ModelViewSet):
    queryset = Shortage.objects.all().order_by('reported_at')
    serializer_class = ShortageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        is_ordered_data = request.data.get('is_ordered')
        if request.user.role != 'Manager' and str(is_ordered_data).lower() == 'true':
            raise ValidationError({"is_ordered": "is_ordered can only be set to True by Manager"})

        return super().update(request, *args, **kwargs)



