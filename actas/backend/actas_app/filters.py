import django_filters
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest

from .models import ActaDefuncion, ActaMatrimonio, ActaNacimiento


class BaseActaFilter(django_filters.FilterSet):
    fecha_desde = django_filters.DateFilter(field_name="fecha_inscripcion", lookup_expr="gte")
    fecha_hasta = django_filters.DateFilter(field_name="fecha_inscripcion", lookup_expr="lte")
    anio = django_filters.NumberFilter(field_name="anio")
    libro = django_filters.CharFilter(field_name="libro")
    folio = django_filters.CharFilter(field_name="folio")
    search = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset


class NacimientoFilter(BaseActaFilter):
    def filter_search(self, queryset, name, value):
        return (
            queryset.annotate(
                similarity=Greatest(
                    TrigramSimilarity("nombres", value),
                    TrigramSimilarity("apellido_paterno", value),
                    TrigramSimilarity("apellido_materno", value),
                    TrigramSimilarity("dni", value),
                )
            )
            .filter(similarity__gt=0.1)
            .order_by("-similarity")
        )

    class Meta:
        model = ActaNacimiento
        fields = ["anio", "libro", "folio", "search"]


class MatrimonioFilter(BaseActaFilter):
    def filter_search(self, queryset, name, value):
        return (
            queryset.annotate(
                similarity=Greatest(
                    TrigramSimilarity("contrayente1_nombre_completo", value),
                    TrigramSimilarity("contrayente2_nombre_completo", value),
                    TrigramSimilarity("contrayente1_dni", value),
                    TrigramSimilarity("contrayente2_dni", value),
                )
            )
            .filter(similarity__gt=0.1)
            .order_by("-similarity")
        )

    class Meta:
        model = ActaMatrimonio
        fields = ["anio", "libro", "folio", "search"]


class DefuncionFilter(BaseActaFilter):
    def filter_search(self, queryset, name, value):
        return (
            queryset.annotate(
                similarity=Greatest(
                    TrigramSimilarity("difunto_nombre_completo", value),
                    TrigramSimilarity("difunto_dni", value),
                )
            )
            .filter(similarity__gt=0.1)
            .order_by("-similarity")
        )

    class Meta:
        model = ActaDefuncion
        fields = ["anio", "libro", "folio", "search"]
