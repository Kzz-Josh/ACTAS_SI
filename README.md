# Gestion de Actas Civiles (Django 5 + DRF + PostgreSQL)

## Requisitos
- Docker Desktop con `docker compose`, o Python 3.12 + PostgreSQL 16.
- Git para clonar el repositorio.

## Arranque rapido con Docker
1. Copia el archivo de entorno:
   `Copy-Item .env.example .env`
2. Si vas a exponer la app fuera de tu equipo, ajusta `DJANGO_ALLOWED_HOSTS` en `.env`.
3. Levanta todo:
   `docker compose up --build`

Con eso el proyecto hace automaticamente:
- espera a que PostgreSQL este disponible
- habilita `pg_trgm`
- ejecuta migraciones
- recolecta estaticos
- crea o actualiza el admin bootstrap definido en `.env`

URLs:
- App/API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs/`
- Redoc: `http://localhost:8000/redoc/`
- Healthcheck: `http://localhost:8000/health/`

Credenciales iniciales por defecto:
- usuario: `admin`
- correo: `admin@actas.local`
- clave: la definida en `DJANGO_SUPERUSER_PASSWORD`

## Configuracion sin Docker
1. Crea la base PostgreSQL y asegurate de que el usuario tenga permisos para crear la extension `pg_trgm`.
2. Crea `.env` desde `.env.example`.
3. En `.env`, cambia `POSTGRES_HOST=db` por `POSTGRES_HOST=localhost` si PostgreSQL corre en tu misma maquina.
4. En PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python actas/backend/manage.py migrate --noinput --settings=config.settings.dev
python actas/backend/manage.py ensure_admin --noinput --settings=config.settings.dev
python actas/backend/manage.py runserver --settings=config.settings.dev
```

## Datos y archivos
- `media/` no se versiona. Si necesitas PDFs ya cargados en otro equipo, copialos manualmente.
- El sistema puede arrancar con `media/` vacio y generar nuevos archivos desde cero.

## Usuarios y roles
- `ADMIN`: CRUD completo y gestion de usuarios y auditoria.
- `DIGITADOR`: CRUD de actas y gestion de PDFs.
- `CONSULTA`: solo lectura y previsualizacion de PDF.

## Endpoints principales
- Auth JWT: `POST /api/auth/login/`, `POST /api/auth/refresh/`
- Actas: `/api/actas/nacimientos/`, `/api/actas/matrimonios/`, `/api/actas/defunciones/`
- Previsualizar PDF: `GET /api/actas/{tipo}/{id}/pdf/preview/`
- Descargar PDF: `GET /api/actas/{tipo}/{id}/pdf/download/`
- Auditoria: `GET /api/auditoria/`

## Notas de seguridad
- Cambia `DJANGO_SECRET_KEY` antes de usar el proyecto en un entorno real.
- Cambia las credenciales por defecto del admin bootstrap.
- Revisa `config/settings/prod.py` antes de publicar en produccion.
