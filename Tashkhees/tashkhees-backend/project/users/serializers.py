from django.contrib.auth import get_user_model
from facilities.models import Laboratory
from rest_framework import serializers

from .models import Doctor, LabAdmin

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields = ["id", "email", "username", "is_doctor", "is_lab_admin","is_staff", "is_active", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user with password."""
    password = serializers.CharField(write_only=True, required=True)
    specialization = serializers.CharField(write_only=True, required=False)
    lab = serializers.PrimaryKeyRelatedField(
        queryset=Laboratory.objects.all(),
        required=False
    )


    class Meta:
        model = User
        fields = ["id", "is_doctor", "is_lab_admin","email", "username", "password", "is_staff", "specialization", "lab"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        is_doctor = validated_data.get("is_doctor", False)
        is_lab_admin = validated_data.get("is_lab_admin", False)
        specialization = validated_data.pop("specialization", None)
        lab = validated_data.pop("lab", None)

        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)

        if is_doctor:
            data = {"user":user.id, "specialization": specialization }
            serilizer = DoctorSerializer(data=data)
            if serilizer.is_valid():
                serilizer.save()
            else:
                raise serializers.ValidationError(serilizer.errors)
        if is_lab_admin and lab:
            data = {"user":user.id, "lab": lab.id }
            serilizer = LabAdminSerializer(data=data)
            if serilizer.is_valid():
                serilizer.save()
            else:
                raise serializers.ValidationError(serilizer.errors)

        user.save()
        return user


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for the Doctor profile."""

    class Meta:
        model = Doctor
        fields = ["user", "specialization"]


class LabAdminSerializer(serializers.ModelSerializer):
    """Serializer for the LabAdmin profile."""

    class Meta:
        model = LabAdmin
        fields = ["user", "lab"]
