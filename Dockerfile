FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory with proper permissions
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Starting Social Media Application..."\n\
echo "Database Host: $DATABASE_HOST"\n\
echo "Redis Host: $REDIS_HOST"\n\
echo "MinIO Endpoint: $MINIO_ENDPOINT"\n\
\n\
# Wait for database with timeout\n\
echo "Waiting for database connection..."\n\
timeout=60\n\
counter=0\n\
while [ $counter -lt $timeout ]; do\n\
    if python manage.py check --database default 2>/dev/null; then\n\
        echo "Database connection successful!"\n\
        break\n\
    fi\n\
    echo "Waiting for database... ($counter/$timeout seconds)"\n\
    sleep 2\n\
    counter=$((counter + 2))\n\
done\n\
\n\
if [ $counter -eq $timeout ]; then\n\
    echo "ERROR: Database connection timeout after $timeout seconds"\n\
    echo "Please check your database configuration and ensure the database is accessible"\n\
    exit 1\n\
fi\n\
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
echo "Starting Django development server..."\n\
exec python manage.py runserver 0.0.0.0:8000\n\
' > /app/startup.sh && chmod +x /app/startup.sh

# Expose port
EXPOSE 8000

# Start command
CMD ["/app/startup.sh"] 