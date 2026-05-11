# Gestión de Actas Civiles (Django 5 + DRF + PostgreSQL)

## Requisitos
- Docker y docker-compose, o Python 3.12 con pip/venv.
- PostgreSQL con extensión `pg_trgm` habilitada para búsquedas tolerantes a errores.

## Configuración local (Docker)
```bash
cp .env.example .env
docker compose up --build
```
La API quedará en `http://localhost:8000`, Swagger en `/docs/`.

## Configuración local (sin Docker)
```bash
python -m venv .venv
. .venv/Scripts/activate  # en Windows
pip install -r requirements.txt
cp .env.example .env
python actas/backend/manage.py migrate --settings=config.settings.dev
python actas/backend/manage.py runserver --settings=config.settings.dev
```

## Usuarios y roles
- `ADMIN`: CRUD completo y gestión de usuarios/auditoría.
- `DIGITADOR`: CRUD de actas y gestión de PDFs (sin usuarios).
- `CONSULTA`: Solo lectura y previsualización de PDF (sin descarga).

## Endpoints principales
- Auth JWT: `POST /api/auth/login/`, `POST /api/auth/refresh/`
- Actas: `/api/actas/nacimientos/`, `/api/actas/matrimonios/`, `/api/actas/defunciones/`
  - Previsualizar PDF: `GET /api/actas/{tipo}/{id}/pdf/preview/`
  - Descargar PDF (ADMIN/DIGITADOR): `GET /api/actas/{tipo}/{id}/pdf/download/`
- Auditoría: `GET /api/auditoria/` (solo ADMIN, listado)

## Migraciones
```bash
python actas/backend/manage.py makemigrations --settings=config.settings.dev
python actas/backend/manage.py migrate --settings=config.settings.dev
```

## Notas de seguridad
- Ajusta `DJANGO_SECRET_KEY` en producción.
- Habilita HTTPS y revisa cabeceras seguras (`SECURE_*`) en `config/settings/prod.py`.
