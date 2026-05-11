from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = "CREATE", "Crear"
        UPDATE = "UPDATE", "Actualizar"
        DELETE = "DELETE", "Eliminar"
        VIEW = "VIEW", "Ver"
        PDF_PREVIEW = "PDF_PREVIEW", "Previsualizar PDF"
        PDF_DOWNLOAD = "PDF_DOWNLOAD", "Descargar PDF"
        PDF_PRINT = "PDF_PRINT", "Imprimir PDF"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    role = models.CharField(max_length=20, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    action = models.CharField(max_length=20, choices=Action.choices)
    acta_type = models.CharField(max_length=50)
    acta_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["acta_type", "acta_id"]),
            models.Index(fields=["action"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.action} {self.acta_type} {self.acta_id}"
