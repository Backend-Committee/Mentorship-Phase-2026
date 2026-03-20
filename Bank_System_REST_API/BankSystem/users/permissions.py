from rest_framework import permissions
from users.models import User


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

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object (user profile) or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == User.Role.ADMIN:
            return True
        return obj == request.user
