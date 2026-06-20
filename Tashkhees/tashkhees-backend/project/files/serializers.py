from rest_framework import serializers
from users.models import User

from .models import File, UploadFile


class UploadFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = UploadFile
        fields = [
            "id",
            "file",
            "receiver",
            "approved",
        ]
        read_only_fields = ["id", "approved"]

    def create(self, validated_data):
        request = self.context["request"]

        file_obj = File.objects.create(
            file=validated_data["file"]
        )

        return UploadFile.objects.create(
            file=file_obj,
            receiver=validated_data["receiver"],
            uploader=request.user,
        )
