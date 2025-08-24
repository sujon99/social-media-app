#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found. Please create one from env.example"
    exit 1
fi

echo "🔍 Connectivity Diagnosis Script"
echo "================================"

# Get service hosts from environment
DATABASE_HOST=${DATABASE_HOST:-localhost}
REDIS_HOST=${REDIS_HOST:-localhost}
MINIO_HOST=${MINIO_HOST:-localhost}

echo "📊 Service Configuration:"
echo "   Database: $DATABASE_HOST:${DATABASE_PORT:-3306}"
echo "   Redis: $REDIS_HOST:${REDIS_PORT:-6379}"
echo "   MinIO: $MINIO_HOST:${MINIO_PORT:-9000}"
echo ""

# Test container network connectivity
echo "🐳 Testing container network connectivity..."

# Test ping from container
echo "Testing ping to $DATABASE_HOST from container..."
docker exec social-media-app ping -c 3 $DATABASE_HOST

# Test port connectivity from container
echo ""
echo "Testing port connectivity from container..."

# MySQL
docker exec social-media-app bash -c "timeout 5 bash -c '</dev/tcp/$DATABASE_HOST/${DATABASE_PORT:-3306}' && echo '✅ MySQL port ${DATABASE_PORT:-3306} is accessible' || echo '❌ MySQL port ${DATABASE_PORT:-3306} is NOT accessible'"

# Redis
docker exec social-media-app bash -c "timeout 5 bash -c '</dev/tcp/$REDIS_HOST/${REDIS_PORT:-6379}' && echo '✅ Redis port ${REDIS_PORT:-6379} is accessible' || echo '❌ Redis port ${REDIS_PORT:-6379} is NOT accessible'"

# MinIO
docker exec social-media-app bash -c "timeout 5 bash -c '</dev/tcp/$MINIO_HOST/${MINIO_PORT:-9000}' && echo '✅ MinIO port ${MINIO_PORT:-9000} is accessible' || echo '❌ MinIO port ${MINIO_PORT:-9000} is NOT accessible'"

# Test host network connectivity
echo ""
echo "🏠 Testing host network connectivity..."

# MySQL from host
timeout 5 bash -c "</dev/tcp/$DATABASE_HOST/${DATABASE_PORT:-3306}" && echo '✅ Host can reach MySQL' || echo '❌ Host cannot reach MySQL'

# Redis from host
timeout 5 bash -c "</dev/tcp/$REDIS_HOST/${REDIS_PORT:-6379}" && echo '✅ Host can reach Redis' || echo '❌ Host cannot reach Redis'

# MinIO from host
timeout 5 bash -c "</dev/tcp/$MINIO_HOST/${MINIO_PORT:-9000}" && echo '✅ Host can reach MinIO' || echo '❌ Host cannot reach MinIO'

# Check container status
echo ""
echo "📊 Container Status:"
docker-compose ps

# Check container logs
echo ""
echo "📋 Recent Application Logs:"
docker-compose logs --tail=20 web

echo ""
echo "🔧 Recommendations:"
echo ""
echo "If container cannot reach services:"
echo "   1. Use host network mode:"
echo "   docker run --rm -it --network host -e DATABASE_HOST=$DATABASE_HOST social-media-app_web"
echo ""
echo "If host cannot reach services:"
echo "   1. Check service status on remote servers"
echo "   2. Verify firewall settings"
echo "   3. Check network configuration"
echo ""
echo "If services are accessible but app fails:"
echo "   1. Check application logs: docker-compose logs -f web"
echo "   2. Verify environment variables in .env file"
echo "   3. Check service credentials"
echo ""
echo "For Docker networking issues:"
echo "   1. Add to docker-compose.yml:"
echo "   extra_hosts:"
echo "     - '$DATABASE_HOST:host-gateway'"
echo "     - '$REDIS_HOST:host-gateway'"
echo "     - '$MINIO_HOST:host-gateway'" 