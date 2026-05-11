from django.http import FileResponse, Http404
from rest_framework import viewsets, decorators, response, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from audits.utils import log_action
from users.models import User

from .models import ActaNacimiento, ActaMatrimonio, ActaDefuncion
from .permissions import ActaPermission
from .serializers import (
    ActaNacimientoSerializer,
    ActaMatrimonioSerializer,
    ActaDefuncionSerializer,
)
from .filters import NacimientoFilter, MatrimonioFilter, DefuncionFilter


def _register_action(request, acta, action):
    log_action(
        request,
        action=action,
        acta_type=acta.__class__.__name__,
        acta_id=acta.pk,
        details={"numero_acta": acta.numero_acta},
    )


class BaseActaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ActaPermission]
    serializer_class = None  # set on subclasses
    filterset_class = None
    search_fields = []
    ordering_fields = ["anio", "created_at", "numero_acta"]

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        acta = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
            oficial_registro=serializer.validated_data.get("oficial_registro", "") or "Sistema",
        )
        _register_action(self.request, acta, "CREATE")

    def perform_update(self, serializer):
        acta = serializer.save(updated_by=self.request.user)
        _register_action(self.request, acta, "UPDATE")

    def perform_destroy(self, instance):
        instance.soft_delete()
        _register_action(self.request, instance, "DELETE")

    @decorators.action(
        detail=True,
        methods=["get"],
        url_path="pdf/preview",
        permission_classes=[AllowAny],
    )
    def pdf_preview(self, request, pk=None):
        # Soporte para token en querystring (token JWT en ?token=) para abrir PDF en popup
        user = request.user
        if not user.is_authenticated:
            token = request.GET.get("token")
            if token:
                authenticator = JWTAuthentication()
                try:
                    validated = authenticator.get_validated_token(token)
                    user = authenticator.get_user(validated)
                    request.user = user
                except Exception:
                    return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_authenticated:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

        acta = self.get_object()
        if not acta.pdf_file or not acta.pdf_file.storage.exists(acta.pdf_file.name):
            raise Http404("PDF no disponible")
        _register_action(request, acta, "PDF_PREVIEW")
        resp = FileResponse(acta.pdf_file.open("rb"), content_type="application/pdf")
        resp["Content-Disposition"] = f'inline; filename="{acta.pdf_file.name.split("/")[-1]}"'
        return resp

    @decorators.action(
        detail=True,
        methods=["get"],
        url_path="pdf/download",
        permission_classes=[AllowAny],
    )
    def pdf_download(self, request, pk=None):
        user = request.user
        if not user.is_authenticated:
            token = request.GET.get("token")
            if token:
                authenticator = JWTAuthentication()
                try:
                    validated = authenticator.get_validated_token(token)
                    user = authenticator.get_user(validated)
                    request.user = user
                except Exception:
                    return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_authenticated:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

        if user.role not in (User.Role.ADMIN, User.Role.DIGITADOR):
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        acta = self.get_object()
        if not acta.pdf_file or not acta.pdf_file.storage.exists(acta.pdf_file.name):
            raise Http404("PDF no disponible")
        _register_action(request, acta, "PDF_DOWNLOAD")
        resp = FileResponse(acta.pdf_file.open("rb"), content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="{acta.pdf_file.name.split("/")[-1]}"'
        return resp


class ActaNacimientoViewSet(BaseActaViewSet):
    queryset = ActaNacimiento.objects.all()
    serializer_class = ActaNacimientoSerializer
    filterset_class = NacimientoFilter
    search_fields = ["nombres", "apellido_paterno", "apellido_materno", "dni"]


class ActaMatrimonioViewSet(BaseActaViewSet):
    queryset = ActaMatrimonio.objects.all()
    serializer_class = ActaMatrimonioSerializer
    filterset_class = MatrimonioFilter
    search_fields = [
        "contrayente1_nombre_completo",
        "contrayente2_nombre_completo",
        "contrayente1_dni",
        "contrayente2_dni",
    ]


class ActaDefuncionViewSet(BaseActaViewSet):
    queryset = ActaDefuncion.objects.all()
    serializer_class = ActaDefuncionSerializer
    filterset_class = DefuncionFilter
    search_fields = ["difunto_nombre_completo", "difunto_dni"]
