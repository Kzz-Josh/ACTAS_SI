from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets, decorators
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    AdminResetPasswordSerializer,
    AdminUserCreateSerializer,
    AdminUserSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "create":
            return AdminUserCreateSerializer
        if self.action == "reset_password":
            return AdminResetPasswordSerializer
        return AdminUserSerializer

    @decorators.action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save(update_fields=["is_active"])
        return Response({"detail": "Usuario desactivado"})

    @decorators.action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response({"detail": "Usuario activado"})

    @decorators.action(detail=True, methods=["post"])
    def reset_password(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response({"detail": "Contraseña actualizada"})


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        reset_link = f"https://example.local/reset?user={user.pk}&ts={timezone.now().timestamp()}"
        send_mail(
            subject="Recuperación de contraseña",
            message=f"Use este enlace para restablecer su contraseña: {reset_link}",
            from_email=None,
            recipient_list=[email],
        )
        return Response({"detail": "Se envió un enlace de restablecimiento."})


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"detail": "Contraseña actual incorrecta."}, status=400)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        update_session_auth_hash(request, user)
        return Response({"detail": "Contraseña actualizada."})


TokenLoginView = TokenObtainPairView
TokenRefresh = TokenRefreshView
