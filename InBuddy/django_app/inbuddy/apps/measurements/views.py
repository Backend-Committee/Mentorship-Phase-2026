from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BodyMeasurement
from .serializers import BodyMeasurementCreateSerializer, BodyMeasurementSerializer


class MeasurementListCreateView(generics.ListCreateAPIView):
    serializer_class = BodyMeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = BodyMeasurement.objects.filter(user=self.request.user)
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BodyMeasurementCreateSerializer
        return BodyMeasurementSerializer


class MeasurementDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BodyMeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BodyMeasurement.objects.filter(user=self.request.user)


class MeasurementLatestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        measurement = BodyMeasurement.objects.filter(user=request.user).first()
        if measurement is None:
            return Response({'detail': 'No measurements found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BodyMeasurementSerializer(measurement)
        return Response(serializer.data)
