from rest_framework import serializers

from .models import Address, Clinic, Laboratory


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "content_type",
            "object_id",
            "governorate",
            "city",
            "street",
            "latitude",
            "longitude",
        ]


class ClinicSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    doctors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Clinic
        fields = [
            "id",
            "name",
            "description",
            "phone",
            "email",
            "website",
            "opening_time",
            "closing_time",
            "is_active",
            "specialty",
            "consultation_fee",
            "emergency_services",
            "appointment_required",
            "doctors",
            "addresses",
        ]


class LaboratorySerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Laboratory
        fields = [
            "id",
            "name",
            "description",
            "phone",
            "email",
            "website",
            "opening_time",
            "closing_time",
            "is_active",
            "home_sample_collection",
            "online_results",
            "addresses",
        ]
