from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UploadFile
from .serializers import UploadFileSerializer


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @transaction.atomic
    def post(self, request):
        serializer = UploadFileSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response({"id": instance.id})


class UnapprovedFilesView(generics.ListAPIView):
    """List all unapproved files sent to the current authenticated user."""

    permission_classes = [IsAuthenticated]
    serializer_class = UploadFileSerializer

    def get_queryset(self):
        return UploadFile.objects.filter(
            receiver=self.request.user,
            approved=False,
        )


class ApprovedFilesView(generics.ListAPIView):
    """List all files the current user has approved."""

    permission_classes = [IsAuthenticated]
    serializer_class = UploadFileSerializer

    def get_queryset(self):
        return UploadFile.objects.filter(
            receiver=self.request.user,
            approved=True,
        )


class ApproveFileView(APIView):
    """Approve a file by ID. Only the receiver can approve."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        upload_file = get_object_or_404(UploadFile, pk=pk)

        if upload_file.receiver != request.user:
            return Response(
                {"detail": "You do not have permission to approve this file."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if upload_file.approved:
            return Response(
                {"detail": "This file has already been approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        upload_file.approved = True
        upload_file.save()

        serializer = UploadFileSerializer(upload_file)
        return Response(serializer.data)
