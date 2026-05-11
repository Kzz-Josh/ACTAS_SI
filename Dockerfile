FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Colocamos el trabajo en la carpeta del backend para que el módulo config sea resoluble.
WORKDIR /app/actas/backend

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
