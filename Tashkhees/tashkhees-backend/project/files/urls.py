from django.urls import path
from .views import (
    ApproveFileView,
    ApprovedFilesView,
    FileUploadView,
    UnapprovedFilesView,
)


urlpatterns = [
    path("", FileUploadView.as_view(), name="file-upload"),
    path("unapproved/", UnapprovedFilesView.as_view(), name="unapproved-files"),
    path("approved/", ApprovedFilesView.as_view(), name="approved-files"),
    path("<int:pk>/approve/", ApproveFileView.as_view(), name="approve-file"),
]
