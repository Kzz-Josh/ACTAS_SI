import pytest
from rest_framework.test import APIRequestFactory

from actas_app.permissions import ActaPermission
from users.models import User


@pytest.mark.django_db
def test_consulta_cannot_modify_actas():
    user = User.objects.create_user(username="c", password="x", role=User.Role.CONSULTA)
    factory = APIRequestFactory()
    request = factory.post("/api/actas/nacimientos/")
    request.user = user
    perm = ActaPermission()
    assert not perm.has_permission(request, None)


@pytest.mark.django_db
def test_digitador_can_create():
    user = User.objects.create_user(username="d", password="x", role=User.Role.DIGITADOR)
    factory = APIRequestFactory()
    request = factory.post("/api/actas/nacimientos/")
    request.user = user
    perm = ActaPermission()
    assert perm.has_permission(request, None)
