from django.contrib import admin

from .models import ActaNacimiento, ActaMatrimonio, ActaDefuncion


@admin.register(ActaNacimiento)
class ActaNacimientoAdmin(admin.ModelAdmin):
    list_display = (
        "numero_acta",
        "nombres",
        "apellido_paterno",
        "apellido_materno",
        "anio",
        "is_active",
    )
    list_filter = ("anio", "is_active")
    search_fields = ("numero_acta", "nombres", "apellido_paterno", "apellido_materno")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")


@admin.register(ActaMatrimonio)
class ActaMatrimonioAdmin(admin.ModelAdmin):
    list_display = (
        "numero_acta",
        "contrayente1_nombre_completo",
        "contrayente2_nombre_completo",
        "anio",
        "is_active",
    )
    list_filter = ("anio", "is_active")
    search_fields = (
        "numero_acta",
        "contrayente1_nombre_completo",
        "contrayente2_nombre_completo",
    )
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")


@admin.register(ActaDefuncion)
class ActaDefuncionAdmin(admin.ModelAdmin):
    list_display = ("numero_acta", "difunto_nombre_completo", "anio", "is_active")
    list_filter = ("anio", "is_active")
    search_fields = ("numero_acta", "difunto_nombre_completo")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
