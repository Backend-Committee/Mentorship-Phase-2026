from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework import generics,mixins
from django.shortcuts import render
from .serializer import *
from .models import *
# Create your views here.
class ListCreateAdhkar(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset=Adhkar.objects.all()
    serializer_class=AdhkarSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'category']
    permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticatedOrReadOnly]

class GetUpdateDeleteAdhkar(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset=Adhkar.objects.all()
    serializer_class=AdhkarSerializer
    permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticatedOrReadOnly]
class ListCategory(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    filter_backends = [SearchFilter]
    search_fields=['name']
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
