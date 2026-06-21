from rest_framework import generics, permissions

from .models import AnalysisResult
from .serializers import AnalysisCreateSerializer, AnalysisResultSerializer
from .services import parse_body_composition


class AnalysisCreateView(generics.CreateAPIView):
    serializer_class = AnalysisCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from analysis.services import parse_body_composition

        validated_data = serializer.validated_data
        text = validated_data.pop('text')
        parsed_metrics = parse_body_composition(text)

        analysis = AnalysisResult.objects.create(
            user=self.request.user,
            source_text=text,
            parsed_metrics=parsed_metrics,
            **validated_data,
        )
        return analysis


class AnalysisListView(generics.ListAPIView):
    serializer_class = AnalysisResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnalysisResult.objects.filter(user=self.request.user)


class AnalysisDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = AnalysisResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnalysisResult.objects.filter(user=self.request.user)
