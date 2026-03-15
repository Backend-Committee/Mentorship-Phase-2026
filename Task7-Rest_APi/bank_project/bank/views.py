from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Account
from .serializers import CustomerSerializer, AccountSerializer


# Create your views here.
@api_view(["POST"])
def create_customer(request):

    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(
        serializer.data,
    )


@api_view(["GET"])
def get_customers(request):

    customers = Customer.objects.all()

    serializer = CustomerSerializer(customers, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def create_account(request):

    serializer = AccountSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
def get_accounts(request):

    accounts = Account.objects.all()

    serializer = AccountSerializer(accounts, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def deposit(request):

    account = Account.objects.get(id=request.data["account_id"])

    amount = float(request.data["amount"])

    account.balance += amount
    account.save()

    return Response({"message": "Deposit successful"})


@api_view(["POST"])
def withdraw(request):

    account = Account.objects.get(id=request.data["account_id"])

    amount = float(request.data["amount"])

    if account.balance < amount:
        return Response({"error": "Insufficient balance"})

    account.balance -= amount
    account.save()

    return Response({"message": "Withdraw successful"})


@api_view(["POST"])
def transfer(request):

    from_account = Account.objects.get(id=request.data["from_account"])
    to_account = Account.objects.get(id=request.data["to_account"])

    amount = float(request.data["amount"])

    if from_account.balance < amount:
        return Response({"error": "Insufficient balance"})

    from_account.balance -= amount
    to_account.balance += amount

    from_account.save()
    to_account.save()

    return Response({"message": "Transfer successful"})