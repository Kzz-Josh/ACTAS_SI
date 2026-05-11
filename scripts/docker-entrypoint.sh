#!/bin/sh
set -eu

cd /app/actas/backend

python - <<'PY'
import os
import sys
import time

import psycopg2

host = os.environ.get("POSTGRES_HOST", "db")
port = int(os.environ.get("POSTGRES_PORT", "5432"))
dbname = os.environ.get("POSTGRES_DB", "actas_db")
user = os.environ.get("POSTGRES_USER", "actas_user")
password = os.environ.get("POSTGRES_PASSWORD", "actas_pass")
max_attempts = int(os.environ.get("DB_WAIT_MAX_ATTEMPTS", "30"))
delay_seconds = int(os.environ.get("DB_WAIT_DELAY_SECONDS", "2"))

for attempt in range(1, max_attempts + 1):
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        connection.close()
        print(f"Database is ready after {attempt} attempt(s).")
        break
    except psycopg2.OperationalError as exc:
        if attempt == max_attempts:
            print(f"Database did not become ready: {exc}", file=sys.stderr)
            sys.exit(1)
        print(f"Waiting for database ({attempt}/{max_attempts}): {exc}")
        time.sleep(delay_seconds)
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py ensure_admin --noinput

exec "$@"
