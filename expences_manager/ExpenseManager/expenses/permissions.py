from rest_framework.permissions import BasePermission

from .models import Panel, PanelUser


class IsPanelOwner(BasePermission):
    """User is the owner of the panel."""

    message = "Only panel owner can perform this action."

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Panel):
            return obj.owner == request.user
        if isinstance(obj, PanelUser):
            return obj.panel.owner == request.user
        return obj.panel.owner == request.user


class IsPanelMember(BasePermission):
    """User is a member of the panel."""

    message = "User is not a member of this panel."

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Panel):
            return PanelUser.objects.filter(user=request.user, panel=obj).exists()
        if isinstance(obj, PanelUser):
            return PanelUser.objects.filter(user=request.user, panel=obj.panel).exists()
        return PanelUser.objects.filter(user=request.user, panel=obj.panel).exists()


class IsPanelOwnerOrEditor(BasePermission):
    """User is panel owner or editor."""

    message = "Only panel owner or editor can perform this action."

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Panel):
            return obj.owner == request.user

        panel = obj if isinstance(obj, Panel) else getattr(obj, "panel", None)
        if not panel:
            return False

        if panel.owner == request.user:
            return True

        try:
            membership = PanelUser.objects.get(user=request.user, panel=panel)
            return membership.role in [PanelUser.Role.OWNER, PanelUser.Role.EDITOR]
        except PanelUser.DoesNotExist:
            return False


class IsPanelMemberReadOnly(BasePermission):
    """User is panel member (owner, editor, or viewer). Viewers get read-only access."""

    message = "User is not a member of this panel."

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            panel = obj if isinstance(obj, Panel) else getattr(obj, "panel", None)
            if not panel:
                return False
            return PanelUser.objects.filter(user=request.user, panel=panel).exists()

        if isinstance(obj, Panel):
            return obj.owner == request.user

        panel = obj if isinstance(obj, Panel) else getattr(obj, "panel", None)
        if not panel:
            return False

        if panel.owner == request.user:
            return True

        try:
            membership = PanelUser.objects.get(user=request.user, panel=panel)
            return membership.role in [PanelUser.Role.OWNER, PanelUser.Role.EDITOR]
        except PanelUser.DoesNotExist:
            return False


class ViewerReadOnly(BasePermission):
    """Viewer role gets read-only access to data."""

    message = "Viewers can only read data."

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        panel = obj if isinstance(obj, Panel) else getattr(obj, "panel", None)
        if not panel:
            return False

        try:
            membership = PanelUser.objects.get(user=request.user, panel=panel)
            return membership.role != PanelUser.Role.VIEWER
        except PanelUser.DoesNotExist:
            return False
