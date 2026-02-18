#!/bin/bash
cd proyecto_clinica
echo "=== Ejecutando migraciones ==="
python manage.py migrate --noinput
echo "=== Recolectando archivos estaticos ==="
python manage.py collectstatic --noinput
echo "=== Iniciando servidor ==="
gunicorn clinica.wsgi --bind 0.0.0.0:$PORT
