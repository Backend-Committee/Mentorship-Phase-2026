from __future__ import annotations

from typing import Any

from .models import AuditLog


def log_audit_event(
    *,
    actor=None,
    panel=None,
    action: str,
    instance=None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    description: str = "",
    metadata: dict[str, Any] | None = None,
    request=None,
):
    if instance is not None:
        entity_type = entity_type or instance._meta.model_name
        entity_id = entity_id or str(instance.pk)
        panel = panel or getattr(instance, "panel", None)

    if request is not None:
        if actor is None and hasattr(request, "user") and getattr(request.user, "is_authenticated", False):
            actor = request.user
        if hasattr(request, "META"):
            metadata = dict(metadata or {})
            forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
            metadata.setdefault("path", request.path)
            metadata.setdefault("method", request.method)
            metadata.setdefault("ip_address", forwarded_for or request.META.get("REMOTE_ADDR"))
            metadata.setdefault("user_agent", request.META.get("HTTP_USER_AGENT", ""))

    AuditLog.objects.create(
        actor=actor,
        panel=panel,
        action=action,
        entity_type=entity_type or "unknown",
        entity_id=entity_id or "unknown",
        description=description,
        metadata=metadata or {},
        ip_address=(metadata or {}).get("ip_address"),
        user_agent=(metadata or {}).get("user_agent", ""),
    )
