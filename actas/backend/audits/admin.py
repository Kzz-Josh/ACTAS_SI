from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "role", "action", "acta_type", "acta_id", "ip_address")
    list_filter = ("action", "acta_type", "role", "timestamp")
    search_fields = ("user__username", "ip_address", "acta_id")
    readonly_fields = [f.name for f in AuditLog._meta.fields]
