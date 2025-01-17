#!/bin/sh


if python manage.py makemigrations --dry-run | grep "No changes detected"; then
    echo "No new migrations to apply."
else
    echo "Making migrations..."
    python manage.py makemigrations
fi


echo "Running migrations..."
python manage.py migrate


echo "Starting Gunicorn server..."
exec gunicorn inventory.wsgi:application --bind 0.0.0.0:8000

