
FROM python:3.9-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up cache to reduce image size


COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/


COPY .env /app/.env


RUN ls /app/manage.py


ENTRYPOINT ["sh", "-c", "gunicorn inventory.wsgi:application --bind 0.0.0.0:8000"]
