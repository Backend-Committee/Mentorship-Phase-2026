from rest_framework.permissions import BasePermission
from User.models import UserRoom
from .models import Room
class IsRoomAdmin(BasePermission):
    def has_permission(self, request, view):
        room_id = view.kwargs.get('room_id')

        # check if room exists first
        if not Room.objects.filter(id=room_id).exists():
            return True  # let the view handle 404

        return Room.objects.filter(
            id=room_id,
            admin=request.user
        ).exists()

class IsRoomMember(BasePermission):
    def has_permission(self, request, view):
        room_id = view.kwargs.get('room_id')
        return UserRoom.objects.filter(
            user    = request.user,
            room_id = room_id
        ).exists()