import re
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_username(self, value: str) -> str:
        if not re.fullmatch(r"^[A-Za-z0-9_]{3,50}$", value):
            raise serializers.ValidationError(
                "Username must be 3-50 chars and use only letters, numbers, and underscores."
            )
        return value

    def validate_password(self, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must include at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must include at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must include at least one digit.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
