#!/bin/bash
set -o errexit

echo "▶ Running collectstatic"
python manage.py collectstatic --noinput

echo "▶ Running migrations"
python manage.py migrate

echo "▶ Starting Gunicorn"
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
