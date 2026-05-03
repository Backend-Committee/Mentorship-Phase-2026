from rest_framework import serializers
from .models import Room
from User.models import UserRoom , User
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'name',
            'reading_deadline',
            'daily_fine'
        )

    def validate_name(self, name):
        if len(name) <4:
            raise serializers.ValidationError(
                "Room name must be at least 4 characters"
            )
        return name
    def validate_daily_fine(self, fine):
        if fine <= 0:
            raise serializers.ValidationError(
                "Fine must be greater than 0"
            )
        return fine


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'username']


class RoomDetailSerializer(serializers.ModelSerializer):
    admin   = SimpleUserSerializer(read_only=True)
    members = serializers.SerializerMethodField()

    class Meta:
        model  = Room
        fields = ['id', 'name', 'reading_deadline', 'daily_fine', 'admin', 'members']

    def get_members(self, obj):
        memberships = UserRoom.objects.filter(room=obj)
        users = [m.user for m in memberships]
        return SimpleUserSerializer(users, many=True).data


class EditRoomSettingsSerializer(RoomSerializer):
    class Meta:
        model = Room
        fields = ['name', 'daily_fine', 'reading_deadline']

class RoomListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = UserRoom
        fields = ['room', 'role'] # add your other fields here

    def get_role(self, obj):
        # 'obj' here is the UserRoom instance
        if obj.room.admin == self.context['request'].user:
            return "admin"
        return "member"