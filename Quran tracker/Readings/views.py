from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import date
from .models import Reading
from .serializers import LogReadingSerializer
from Room.models import Room
from Room.permissions import IsRoomMember

class LogReadingView(APIView):
    permission_classes = [IsAuthenticated, IsRoomMember]

    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)

        # check if user already logged today
        already_logged = Reading.objects.filter(
            user              = request.user,
            room              = room,
            reading_date_time = date.today()
        ).exists()

        if already_logged:
            return Response(
                {'error': 'You have already logged your reading today'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LogReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user = request.user,
                room = room,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)