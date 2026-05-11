from django.http import HttpRequest

from .models import AuditLog


def log_action(request: HttpRequest, action: str, acta_type: str, acta_id: int, details=None):
    user = getattr(request, "user", None)
    role = getattr(user, "role", "") if user and user.is_authenticated else ""
    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        role=role,
        ip_address=_get_client_ip(request),
        action=action,
        acta_type=acta_type,
        acta_id=acta_id,
        details=details or {},
    )


def _get_client_ip(request: HttpRequest) -> str | None:
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
