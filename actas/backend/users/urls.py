from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AdminUserViewSet,
    MeView,
    PasswordChangeView,
    PasswordResetView,
    RegisterView,
    TokenLoginView,
    TokenRefresh,
)

router = DefaultRouter()
router.register(r"users", AdminUserViewSet, basename="admin-users")

urlpatterns = [
    path("login/", TokenLoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefresh.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password-change/", PasswordChangeView.as_view(), name="password_change"),
    path("", include(router.urls)),
]
