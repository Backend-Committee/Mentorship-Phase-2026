from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer , CustomerCreateSerializer , CustomerUpdateSerializer
# Create your views here.

class ListCreateCustomers(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerCreateSerializer
        return CustomerSerializer


class DeleteUpdateCustomer(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    lookup_field = 'id'
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CustomerUpdateSerializer
        return CustomerSerializer