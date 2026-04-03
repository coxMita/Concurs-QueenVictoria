#!/bin/sh
set -e

mkdir -p /app/data /app/data/media /app/staticfiles

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
