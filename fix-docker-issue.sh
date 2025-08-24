#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found. Please create one from env.example"
    exit 1
fi

echo "🔧 Docker Issue Fix Script"
echo "=========================="

# Function to test connectivity
test_connectivity() {
    local host=$1
    local port=$2
    local service=$3
    
    echo "Testing $service connection to $host:$port..."
    if timeout 5 bash -c "</dev/tcp/$host/$port" 2>/dev/null; then
        echo "✅ $service connection successful"
        return 0
    else
        echo "❌ $service connection failed"
        return 1
    fi
}

# Test external service connectivity
echo "🔍 Testing external service connectivity..."

# Test MySQL
test_connectivity "${DATABASE_HOST:-localhost}" "${DATABASE_PORT:-3306}" "MySQL"
mysql_status=$?

# Test Redis
test_connectivity "${REDIS_HOST:-localhost}" "${REDIS_PORT:-6379}" "Redis"
redis_status=$?

# Test MinIO
test_connectivity "${MINIO_HOST:-localhost}" "${MINIO_PORT:-9000}" "MinIO"
minio_status=$?

# Check if all services are accessible
if [ $mysql_status -eq 0 ] && [ $redis_status -eq 0 ] && [ $minio_status -eq 0 ]; then
    echo "✅ All external services are accessible"
else
    echo "❌ Some external services are not accessible"
    echo "Please check:"
    echo "   1. Network connectivity to your service hosts"
    echo "   2. Service status on remote servers"
    echo "   3. Firewall settings"
    exit 1
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null

# Clean up Docker resources
echo "🧹 Cleaning up Docker resources..."
docker system prune -f

# Rebuild images
echo "🔨 Rebuilding Docker images..."
docker-compose build --no-cache

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Check service status
echo "📊 Checking service status..."
docker-compose ps

# Check logs
echo "📋 Checking application logs..."
docker-compose logs --tail=50 web

# Test application health
echo "🏥 Testing application health..."
if curl -f http://localhost:8000/ >/dev/null 2>&1; then
    echo "✅ Application is responding"
else
    echo "❌ Application is not responding"
    echo "Checking detailed logs..."
    docker-compose logs web
fi

echo ""
echo "🔧 Troubleshooting completed!"
echo ""
echo "If issues persist:"
echo "   1. Check the logs: docker-compose logs -f"
echo "   2. Verify .env file configuration"
echo "   3. Ensure external services are running"
echo "   4. Check network connectivity" 