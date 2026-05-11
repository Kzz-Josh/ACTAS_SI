from typing import Any

from django.urls import reverse
from rest_framework import serializers

from .models import ActaDefuncion, ActaMatrimonio, ActaNacimiento


class ActaBaseSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        fields = [
            "id",
            "tipo_acta",
            "numero_acta",
            "libro",
            "folio",
            "anio",
            "oficial_registro",
            "fecha_inscripcion",
            "observaciones",
            "pdf_file",
            "pdf_url",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "tipo_acta", "created_at", "updated_at", "is_active", "pdf_url"]

    def get_pdf_url(self, obj: Any) -> str | None:
        request = self.context.get("request")
        view = self.context.get("view")
        if obj.pdf_file and request and view:
            view_name = f"{view.basename}-pdf-preview"
            return request.build_absolute_uri(reverse(view_name, kwargs={"pk": obj.pk}))
        return None


class ActaNacimientoSerializer(ActaBaseSerializer):
    class Meta(ActaBaseSerializer.Meta):
        model = ActaNacimiento
        fields = ActaBaseSerializer.Meta.fields + [
            "distrito",
            "nombres",
            "apellido_paterno",
            "apellido_materno",
            "fecha_nacimiento",
        ]

    def create(self, validated_data):
        validated_data["tipo_acta"] = "nacimiento"
        return super().create(validated_data)

    def validate(self, data):
        required = ["nombres", "apellido_paterno", "apellido_materno", "fecha_nacimiento", "distrito"]
        missing = [field for field in required if not data.get(field)]
        if missing:
            raise serializers.ValidationError({field: "Requerido" for field in missing})
        return data


class ActaMatrimonioSerializer(ActaBaseSerializer):
    class Meta(ActaBaseSerializer.Meta):
        model = ActaMatrimonio
        fields = ActaBaseSerializer.Meta.fields + [
            "contrayente1_nombre_completo",
            "contrayente2_nombre_completo",
            "fecha_matrimonio",
        ]

    def create(self, validated_data):
        validated_data["tipo_acta"] = "matrimonio"
        return super().create(validated_data)

    def validate(self, data):
        required = ["contrayente1_nombre_completo", "contrayente2_nombre_completo", "fecha_matrimonio"]
        missing = [field for field in required if not data.get(field)]
        if missing:
            raise serializers.ValidationError({field: "Requerido" for field in missing})
        return data


class ActaDefuncionSerializer(ActaBaseSerializer):
    class Meta(ActaBaseSerializer.Meta):
        model = ActaDefuncion
        fields = ActaBaseSerializer.Meta.fields + [
            "difunto_nombre_completo",
            "fecha_defuncion",
        ]

    def create(self, validated_data):
        validated_data["tipo_acta"] = "defuncion"
        return super().create(validated_data)

    def validate(self, data):
        required = ["difunto_nombre_completo", "fecha_defuncion"]
        missing = [field for field in required if not data.get(field)]
        if missing:
            raise serializers.ValidationError({field: "Requerido" for field in missing})
        return data
