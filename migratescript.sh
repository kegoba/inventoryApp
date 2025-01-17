#!/bin/sh
if python manage.py showmigrations | grep '\[ \]'; then
    echo "Running migrations..."
    python manage.py migrate
else
    echo "Migrations already applied."
fi


echo "Starting Gunicorn server..."
exec gunicorn inventory.wsgi:application --bind 0.0.0.0:8000
