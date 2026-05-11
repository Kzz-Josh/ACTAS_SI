import pytest
from django.test import RequestFactory

from audits.models import AuditLog
from audits.utils import log_action
from users.models import User


@pytest.mark.django_db
def test_log_action_records_role_and_user():
    user = User.objects.create_user(username="admin", password="x", role=User.Role.ADMIN)
    request = RequestFactory().get("/api/actas/nacimientos/1/")
    request.user = user

    log_action(request, action="VIEW", acta_type="ActaNacimiento", acta_id=1)

    entry = AuditLog.objects.first()
    assert entry is not None
    assert entry.user == user
    assert entry.role == User.Role.ADMIN
    assert entry.acta_id == 1
    assert entry.action == "VIEW"
