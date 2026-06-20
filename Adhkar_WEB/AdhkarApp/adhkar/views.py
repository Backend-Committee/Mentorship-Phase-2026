from rest_framework import generics, mixins
from rest_framework.filters import SearchFilter
from .serializer import *
from .models import *
from .permissions import ReadOnlyOrAdmin

class ListCreateAdhkar(generics.ListCreateAPIView):
    queryset = Adhkar.objects.all()
    serializer_class = AdhkarSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'category__name']
    permission_classes = [ReadOnlyOrAdmin]
    
class GetUpdateDeleteAdhkar(generics.RetrieveUpdateDestroyAPIView):
    queryset = Adhkar.objects.all()
    serializer_class = AdhkarSerializer
    permission_classes = [ReadOnlyOrAdmin]

class ListCreateCategory(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    permission_classes = [ReadOnlyOrAdmin]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAdmin]