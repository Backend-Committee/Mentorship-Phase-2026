from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Facility(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Address(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    facility = GenericForeignKey("content_type", "object_id")

    governorate = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Clinic(Facility):
    specialty = models.CharField(max_length=255, blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    emergency_services = models.BooleanField(default=False)
    appointment_required = models.BooleanField(default=True)
    doctors = models.ManyToManyField(
        "users.Doctor",
        related_name="clinics",
    )


class Laboratory(Facility):
    home_sample_collection = models.BooleanField(default=False)
    online_results = models.BooleanField(default=False)
