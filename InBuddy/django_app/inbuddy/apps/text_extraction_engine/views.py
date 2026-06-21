import logging

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import ExtractionTask
from .serializers import ExtractionCreateSerializer, ExtractionTaskSerializer
from .services import OCRService

logger = logging.getLogger(__name__)


class ExtractionTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = ExtractionTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExtractionTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user, status='processing')
        self._process_task(task)

    def _process_task(self, task):
        try:
            text = OCRService.extract_text(task.image.path)
            task.extracted_text = text
            task.status = 'completed'
            task.save(update_fields=['extracted_text', 'status', 'updated_at'])
        except Exception as e:
            logger.exception(f'Extraction failed for task {task.pk}')
            task.status = 'failed'
            task.error_message = str(e)
            task.save(update_fields=['status', 'error_message', 'updated_at'])


class ExtractionTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExtractionTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExtractionTask.objects.filter(user=self.request.user)
