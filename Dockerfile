# --- Base image ---
FROM python:3.12-slim

# Prevent .pyc files & enable unbuffered logging (good for docker logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (CSS etc.) into STATIC_ROOT
RUN python manage.py collectstatic --noinput

# Expose Django's default port
EXPOSE 8000

# Run migrations then start gunicorn (production server)
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn todoproject.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
