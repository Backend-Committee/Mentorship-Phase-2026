from rest_framework import serializers
from .models import User, UserRoom

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'profile_image'
        )

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError(
                "Username must be at least 4 characters"
            )
        return value

    # validate single field
    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError(
                "Only Gmail addresses are allowed"
            )
        return value

    # validate multiple fields together
    def validate(self, data):
        if data['username'] == data['password']:
            raise serializers.ValidationError(
                "Username and password cannot be the same"
            )
        return data

    def create(self, validated_data):
        newUser = User(
            username=validated_data['username'],
            email=validated_data['email'],
            profile_image=validated_data.get('profile_image', None)
        )
        newUser.set_password(validated_data['password'])
        newUser.save()
        return newUser
