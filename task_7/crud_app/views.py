from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import response
from .serializers import StaffSerializer, CustomerSerializer, AccountTypeSerializer, AccountSerializer
from .models import Staff, Customer, AccountType, Account


class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    queryset = Staff.objects.select_related("person__user").all()

    def destroy(self, request, *args, **kwargs):
        staff = self.get_object()
        if staff.person.user is not None:
            staff.person.user.delete()
        staff.person.delete()
        staff.delete()
        return response.Response(status=204) # 204 is no content response


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.select_related("person__user").all()

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        if customer.person.user is not None:
            customer.person.user.delete()
        customer.person.delete()
        customer.delete()
        return response.Response(status=204) # 204 is no content response


class AccountTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AccountTypeSerializer
    queryset = AccountType.objects.all()


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()