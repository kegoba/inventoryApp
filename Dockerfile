FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the app's port
EXPOSE 8000

# Start the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "inventoryApp.wsgi:application"]
