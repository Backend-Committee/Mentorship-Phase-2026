from rest_framework import serializers
from .models import *

class AdhkarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adhkar
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):   
    adhkar_count = serializers.IntegerField(source='adhkar_list.count', read_only=True)    
    class Meta:
        model = Category
        fields = ['name', 'description', 'adhkar_count']