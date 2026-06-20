from django.db import models

# Create your models here.


class File(models.Model):
    file = models.FileField(upload_to="media/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class UploadFile(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="receive"
    )
    uploader = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="uploade"
    )
    approved = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"file from {self.uploader.username} to {self.receiver.username} -- {self.file.id}"
