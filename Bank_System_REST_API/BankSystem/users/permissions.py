from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.CUSTOMER

class IsTeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.TELLER

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.MANAGER

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.ADMIN

class IsAuditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.AUDITOR

class IsOfficeStaff(permissions.BasePermission):
    """
    Combines Teller, Manager, Admin, Auditor.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            User.Role.TELLER,
            User.Role.MANAGER,
            User.Role.ADMIN,
            User.Role.AUDITOR
        ]
