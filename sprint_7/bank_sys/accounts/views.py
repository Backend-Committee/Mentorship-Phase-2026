from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Account
from .serializers import CustomSerializer, AccountSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

# class CustomerViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserListCreate(APIView):

    def post(self,request):
        serializer = CustomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        serializer = CustomSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

class UserDetails(APIView):

    def get(self, request, pk):
        customer = get_object_or_404(User, pk=pk)
        serializer = CustomSerializer(customer)
        return Response(serializer.data)

    def put(self,request,pk):
        customer = get_object_or_404(User, pk=pk)
        serializer = CustomSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        customer = get_object_or_404(User, pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

########################################################################################
class AccountListCreate(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer




