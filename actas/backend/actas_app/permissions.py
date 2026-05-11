from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import User


class ActaPermission(BasePermission):
    message = "No tiene permisos para esta acción."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = request.user.role
        if request.method in SAFE_METHODS:
            return role in (
                User.Role.ADMIN,
                User.Role.DIGITADOR,
                User.Role.CONSULTA,
            )
        if request.method in ("POST", "PUT", "PATCH"):
            return role in (User.Role.ADMIN, User.Role.DIGITADOR)
        if request.method == "DELETE":
            return role in (User.Role.ADMIN, User.Role.DIGITADOR)
        return False
