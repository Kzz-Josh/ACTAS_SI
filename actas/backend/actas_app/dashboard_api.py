from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from audits.models import AuditLog
from users.models import User

from .models import ActaDefuncion, ActaMatrimonio, ActaNacimiento


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.user.role
        can_audit = role in (User.Role.ADMIN, User.Role.DIGITADOR)
        cache_key = f"dashboard_summary:{role}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        nac_count = ActaNacimiento.active.count()
        mat_count = ActaMatrimonio.active.count()
        def_count = ActaDefuncion.active.count()
        users_count = User.objects.count()

        audit_logs = []
        if can_audit:
            audit_logs = list(
                AuditLog.objects.select_related("user")
                .values(
                    "id",
                    "action",
                    "role",
                    "acta_type",
                    "acta_id",
                    "timestamp",
                    "ip_address",
                    "details",
                    "user__username",
                )[:20]
            )

        payload = {
            "counts": {
                "nacimientos": nac_count,
                "matrimonios": mat_count,
                "defunciones": def_count,
                "total_archivos": nac_count + mat_count + def_count,
            },
            "users_count": users_count,
            "audit_logs": audit_logs,
            "audit_enabled": can_audit,
        }

        # Cache muy corto para mejorar UX sin desactualizar demasiado.
        cache.set(cache_key, payload, timeout=3)
        return Response(payload)
