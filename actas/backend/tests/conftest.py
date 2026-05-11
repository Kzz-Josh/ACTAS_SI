import pytest
from django.db import connection


@pytest.fixture(scope="session", autouse=True)
def ensure_pg_trgm(django_db_blocker):
    """Ensure pg_trgm is available in the test database for trigram indexes."""
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
