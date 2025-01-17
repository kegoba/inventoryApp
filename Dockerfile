# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set environment variables to avoid writing .pyc files and to flush output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up cache to reduce image size

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Copy the .env file to the container
COPY .env /app/.env

# Ensure the `manage.py` file exists in the app directory before running migrations
RUN ls /app/manage.py

# Use an entrypoint script to handle migration and Gunicorn startup
ENTRYPOINT ["sh", "-c", "gunicorn inventory.wsgi:application --bind 0.0.0.0:8000"]
