import re
from rest_framework import serializers

from .models import Panel, PanelUser, Category


class PanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panel
        fields = ["id", "name", "owner", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class PanelUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanelUser
        fields = ["user", "panel", "role", "invited_by", "joined_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "panel", "name", "color_hex", "is_default", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        panel = attrs.get("panel") or getattr(self.instance, "panel", None)
        name = attrs.get("name") or getattr(self.instance, "name", None)
        if panel and name:
            qs = Category.objects.filter(panel=panel, name__iexact=name)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"name": "Category name must be unique within panel."})

        color_hex = attrs.get("color_hex")
        if color_hex and not re.fullmatch(r"^#[0-9A-Fa-f]{6}$", color_hex):
            raise serializers.ValidationError({"color_hex": "Must be a valid hex color like #1A2B3C."})

        return attrs
