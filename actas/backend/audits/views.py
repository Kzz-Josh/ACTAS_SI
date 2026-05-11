from rest_framework import generics, permissions

from users.models import User

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AuditLog.objects.all()
    filterset_fields = ["action", "acta_type", "role"]
    search_fields = ["ip_address"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return AuditLog.objects.none()
        if user.role in (User.Role.ADMIN, User.Role.DIGITADOR):
            return super().get_queryset().select_related("user")
        return AuditLog.objects.none()
