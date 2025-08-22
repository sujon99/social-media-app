# Multi-stage Dockerfile for Django Social Media Application
# Stage 1: Build stage
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=social_media.settings \
    PYTHONPATH=/app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r django && useradd -r -g django django

# Create app directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/logs && \
    chown -R django:django /app

# Install additional production dependencies
RUN pip install gunicorn

# Create production settings file
RUN echo 'import os\n\
from .settings import *\n\
\n\
# Production settings\n\
DEBUG = False\n\
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")\n\
\n\
# Security settings\n\
SECURE_BROWSER_XSS_FILTER = True\n\
SECURE_CONTENT_TYPE_NOSNIFF = True\n\
X_FRAME_OPTIONS = "DENY"\n\
SECURE_HSTS_SECONDS = 31536000\n\
SECURE_HSTS_INCLUDE_SUBDOMAINS = True\n\
SECURE_HSTS_PRELOAD = True\n\
\n\
# Static files\n\
STATIC_ROOT = "/app/static"\n\
\n\
# Logging\n\
LOGGING = {\n\
    "version": 1,\n\
    "disable_existing_loggers": False,\n\
    "formatters": {\n\
        "verbose": {\n\
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",\n\
            "style": "{",\n\
        },\n\
    },\n\
    "handlers": {\n\
        "file": {\n\
            "level": "INFO",\n\
            "class": "logging.FileHandler",\n\
            "filename": "/app/logs/django.log",\n\
            "formatter": "verbose",\n\
        },\n\
    },\n\
    "root": {\n\
        "handlers": ["file"],\n\
        "level": "INFO",\n\
    },\n\
}\n\
' > /app/social_media/production.py

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Wait for database\n\
echo "Waiting for database..."\n\
while ! python manage.py check --database default 2>&1; do\n\
    sleep 1\n\
done\n\
echo "Database is ready!"\n\
\n\
# Run migrations\n\
echo "Running database migrations..."\n\
python manage.py migrate --noinput\n\
\n\
# Collect static files\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput\n\
\n\
# Start application\n\
echo "Starting application..."\n\
exec gunicorn social_media.wsgi:application \\\n\
    --bind 0.0.0.0:8000 \\\n\
    --workers 3 \\\n\
    --worker-class gunicorn.workers.sync.SyncWorker \\\n\
    --worker-connections 1000 \\\n\
    --max-requests 1000 \\\n\
    --max-requests-jitter 100 \\\n\
    --timeout 30 \\\n\
    --keep-alive 2 \\\n\
    --access-logfile /app/logs/access.log \\\n\
    --error-logfile /app/logs/error.log \\\n\
    --log-level info\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Create health check script
RUN echo '#!/bin/bash\n\
curl -f http://localhost:8000/ || exit 1\n\
' > /app/healthcheck.sh && chmod +x /app/healthcheck.sh

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD /app/healthcheck.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"] 