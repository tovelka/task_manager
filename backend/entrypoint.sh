#!/bin/bash
set -e

# Если передана команда — выполняем её
if [ "$1" = "--makemigration" ]; then
    shift
    echo "Creating migration: $1"
    python manage.py --makemigration "$1"
    exit 0
elif [ "$1" = "--migrate" ]; then
    echo "Applying migrations..."
    python manage.py --migrate
    exit 0
elif [ "$1" = "--createsuperuser" ]; then
    python create_superuser.py
    exit 0
elif [ "$1" = "--shell" ]; then
    exec /bin/bash
fi

echo "Make migrations..."
python manage.py --makemigration 'Init migrations'

echo "Running migrations..."
python manage.py --migrate

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload