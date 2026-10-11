#!/bin/bash
set -e

echo "🔄 Ejecutando migraciones..."
flask db upgrade

echo "🚀 Iniciando Gunicorn..."
exec gunicorn --bind 0.0.0.0:8080 \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    "app:create_app()"