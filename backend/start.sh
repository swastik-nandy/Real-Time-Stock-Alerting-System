#!/bin/bash
set -o errexit

echo "▶ Running collectstatic"
python manage.py collectstatic --noinput

echo "▶ Running migrations"
python manage.py migrate --noinput

echo "▶ Starting Gunicorn"
exec gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT &

# Wait a few seconds to let the server start, then perform health check
sleep 5
echo "🩺 Health check:"
curl --fail http://localhost:$PORT/health/ || echo "❌ Health check failed"
wait
