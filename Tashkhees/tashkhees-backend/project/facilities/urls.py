from django.urls import path

from .views import (
    AddressDetailView,
    AddressListView,
    ClinicDetailView,
    ClinicListView,
    LaboratoryDetailView,
    LaboratoryListView,
)

urlpatterns = [
    path("clinics/", ClinicListView.as_view(), name="clinic-list"),
    path("clinics/<int:pk>/", ClinicDetailView.as_view(), name="clinic-detail"),
    path("laboratories/", LaboratoryListView.as_view(), name="laboratory-list"),
    path("laboratories/<int:pk>/", LaboratoryDetailView.as_view(), name="laboratory-detail"),
    path("addresses/", AddressListView.as_view(), name="address-list"),
    path("addresses/<int:pk>/", AddressDetailView.as_view(), name="address-detail"),
]
