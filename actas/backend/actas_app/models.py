from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from simple_history.models import HistoricalRecords


def pdf_upload_path(instance: models.Model, filename: str) -> str:
    acta_type = instance.__class__.__name__.lower()
    return f"pdfs/{acta_type}/{instance.numero_acta}_{filename}"


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ActaBase(models.Model):
    tipo_acta = models.CharField(max_length=50)
    numero_acta = models.CharField(max_length=50)
    libro = models.CharField(max_length=50)
    folio = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    oficial_registro = models.CharField(max_length=150, blank=True, default="")
    fecha_inscripcion = models.DateField()
    observaciones = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to=pdf_upload_path, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["anio"]),
            models.Index(fields=["tipo_acta"]),
            models.Index(fields=["numero_acta"]),
        ]
        ordering = ["-created_at"]

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])


class ActaNacimiento(ActaBase):
    distrito = models.CharField(max_length=150, blank=True)
    nombres = models.CharField(max_length=150)
    apellido_paterno = models.CharField(max_length=150)
    apellido_materno = models.CharField(max_length=150)
    dni = models.CharField(max_length=12, blank=True)
    sexo = models.CharField(max_length=10, blank=True)
    fecha_nacimiento = models.DateField()
    lugar_nacimiento = models.CharField(max_length=200, blank=True)
    padre_nombre_completo = models.CharField(max_length=200, blank=True)
    madre_nombre_completo = models.CharField(max_length=200, blank=True)

    history = HistoricalRecords()

    class Meta(ActaBase.Meta):
        indexes = ActaBase.Meta.indexes + [
            GinIndex(fields=["nombres"], name="idx_nac_nombres_trgm", opclasses=["gin_trgm_ops"]),
            GinIndex(
                fields=["apellido_paterno"], name="idx_nac_ap_trgm", opclasses=["gin_trgm_ops"]
            ),
            GinIndex(
                fields=["apellido_materno"], name="idx_nac_am_trgm", opclasses=["gin_trgm_ops"]
            ),
        ]

    def __str__(self):
        return f"Nacimiento {self.numero_acta} - {self.nombres} {self.apellido_paterno}"


class ActaMatrimonio(ActaBase):
    contrayente1_nombre_completo = models.CharField(max_length=200)
    contrayente1_dni = models.CharField(max_length=12, blank=True)
    contrayente2_nombre_completo = models.CharField(max_length=200)
    contrayente2_dni = models.CharField(max_length=12, blank=True)
    fecha_matrimonio = models.DateField()
    lugar_matrimonio = models.CharField(max_length=200, blank=True)

    history = HistoricalRecords()

    class Meta(ActaBase.Meta):
        indexes = ActaBase.Meta.indexes + [
            GinIndex(
                fields=["contrayente1_nombre_completo"],
                name="idx_mat_c1_trgm",
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                fields=["contrayente2_nombre_completo"],
                name="idx_mat_c2_trgm",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        return f"Matrimonio {self.numero_acta} - {self.contrayente1_nombre_completo}"


class ActaDefuncion(ActaBase):
    difunto_nombre_completo = models.CharField(max_length=200)
    difunto_dni = models.CharField(max_length=12, blank=True)
    fecha_defuncion = models.DateField()
    lugar_defuncion = models.CharField(max_length=200, blank=True)
    causa_muerte = models.CharField(max_length=200, blank=True)

    history = HistoricalRecords()

    class Meta(ActaBase.Meta):
        indexes = ActaBase.Meta.indexes + [
            GinIndex(
                fields=["difunto_nombre_completo"],
                name="idx_def_difunto_trgm",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        return f"Defunción {self.numero_acta} - {self.difunto_nombre_completo}"
