from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'hourly_rate': {'read_only': True},
            'hours': {'read_only': True},
        }
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError({'phone': 'Phone number must be digits!'})
        elif value.len() != 11:
            raise serializers.ValidationError({'phone': 'Phone number must be 11!'})
        elif value.startswith('011', '012', '015', '010'):
            raise serializers.ValidationError({'phone': 'not an Egyptian phone number!'})
        return value