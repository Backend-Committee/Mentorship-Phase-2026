from rest_framework import permissions

from banks.models import BankAdmin  # adjust import


class IsBankAdmin(permissions.BasePermission):
    """
    Allows access only to users who are BankAdmin for a bank.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be a Bank object or anything that has 'bank' attribute
        """
        if request.user.is_superuser:
            return True

        bank = getattr(obj, 'bank', None)
        if bank is None:
            return False

        return BankAdmin.objects.filter(user=request.user, bank=bank).exists()

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to staff or superuser.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class IsAccountOwner(permissions.BasePermission):
    """
    Grants access only if the authenticated user owns the account.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj must be a BankAccount instance
        """
        if request.user.is_superuser:
            return True

        return obj.user == request.user
