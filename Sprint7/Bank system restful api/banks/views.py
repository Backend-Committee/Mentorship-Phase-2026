

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from banks.models import Bank, BankAccount
from banks.permissions import IsBankAdmin
from banks.serializers import BankAccountSerializer, BankSerializer


class BankListCreateView(generics.ListCreateAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    def get_permissions(self):
        """
        Return permission classes based on request method
        """
        if self.request.method == "GET":
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class BankRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    def get_permissions(self):
        """
        Return permission classes based on request method
        """
        if self.request.method == "GET":
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

class BankAccountListCreateView(generics.ListCreateAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsBankAdmin]

    def get_queryset(self):
        bank_id = self.kwargs.get("bank_id")
        return BankAccount.objects.filter(bank=bank_id)

    def perform_create(self, serializer):
        serializer.save(
            bank_id=self.kwargs.get("bank_id"),
            user=self.request.user,
            balance=self.request.data.get("balance", 0),
        )

class BankAccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsBankAdmin]
