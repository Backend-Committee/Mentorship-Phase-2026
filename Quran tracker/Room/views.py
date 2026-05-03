from django.shortcuts import get_object_or_404
from .models import Room
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (RoomSerializer, RoomDetailSerializer, SimpleUserSerializer,
                          EditRoomSettingsSerializer, RoomListSerializer)
from .permissions import IsRoomAdmin
from User.models import UserRoom
# Create your views here.

class RoomCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request):
        serializer = RoomSerializer(data= request.data)

        if serializer.is_valid():
            try:
                from django.db import transaction
                with transaction.atomic():
                    room = serializer.save(admin=request.user)
                    UserRoom.objects.create(
                        user= request.user,
                        room = room,
                        total_fine = 0
                    )
                return Response(
                    {
                        "id": room.id,
                        "room": room.name,
                        "daily_fine": room.daily_fine,
                        "reading_deadline": room.reading_deadline,
                        "admin": room.admin.username if room.admin else None,
                        "message": "Room created successfully"
                    },
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = UserRoom.objects.filter(user=request.user)
        serializer = RoomListSerializer(rooms, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user_room_entry = UserRoom.objects.get(user=request.user, room_id=pk)
            room = user_room_entry.room

            serializer = RoomDetailSerializer(room)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserRoom.DoesNotExist:
            return Response({"detail": "Room not found or no access"}, status=404)


class EditRoomSettingsView(APIView):
    permission_classes = [IsAuthenticated, IsRoomAdmin]
    def patch(self, request, room_id):
        # temporary debug lines
        room_check = Room.objects.filter(id=room_id, admin=request.user).first()
        room = get_object_or_404(Room, id=room_id)
        serializer = EditRoomSettingsSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)