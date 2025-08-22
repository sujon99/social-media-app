#!/bin/bash

echo "🔧 Fixing MySQL Connection Issue"
echo "================================"

# Stop the current container
echo "🛑 Stopping current container..."
docker-compose -f docker-compose.simple.yml down

# Clean up any hanging containers
echo "🧹 Cleaning up Docker resources..."
docker system prune -f

# Test host connectivity first
echo "🔍 Testing host connectivity to external services..."
echo "Testing MySQL connection to 192.168.91.110:3306..."
if timeout 5 bash -c '</dev/tcp/192.168.91.110/3306' 2>/dev/null; then
    echo "✅ Host can reach MySQL - proceeding with fix"
else
    echo "❌ Host cannot reach MySQL - check your network configuration"
    echo "Make sure 192.168.91.110 is accessible from this machine"
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs static

# Build and start with fixed configuration
echo "🔨 Building with fixed network configuration..."
docker-compose -f docker-compose.fixed.yml build

if [ $? -ne 0 ]; then
    echo "❌ Build failed - check the error messages above"
    exit 1
fi

echo "🚀 Starting service with fixed network configuration..."
docker-compose -f docker-compose.fixed.yml up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start service - check the error messages above"
    exit 1
fi

# Wait for service to start
echo "⏳ Waiting for service to start..."
sleep 20

# Check service status
echo "📊 Checking service status..."
if docker ps | grep -q "social-media-app"; then
    echo "✅ Service is running"
else
    echo "❌ Service failed to start"
    echo "Checking logs..."
    docker-compose -f docker-compose.fixed.yml logs web
    exit 1
fi

# Test connectivity from container
echo "🌐 Testing connectivity from container..."
echo "Testing MySQL connection from container..."
docker exec social-media-app bash -c "timeout 5 bash -c '</dev/tcp/192.168.91.110/3306' && echo '✅ Container can reach MySQL' || echo '❌ Container cannot reach MySQL'"

# Run migrations
echo "🗄️ Running database migrations..."
docker-compose -f docker-compose.fixed.yml exec web python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ Migrations failed - check the error messages above"
    exit 1
fi

# Collect static files
echo "📁 Collecting static files..."
docker-compose -f docker-compose.fixed.yml exec web python manage.py collectstatic --noinput

if [ $? -ne 0 ]; then
    echo "❌ Static file collection failed - check the error messages above"
    exit 1
fi

echo ""
echo "🎉 MySQL Connection Issue Fixed!"
echo ""
echo "📱 Access your application at:"
echo "   - Main App: http://localhost:8000"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: docker-compose -f docker-compose.fixed.yml logs -f web"
echo "   - Stop service: docker-compose -f docker-compose.fixed.yml down"
echo "   - Create superuser: docker-compose -f docker-compose.fixed.yml exec web python manage.py createsuperuser"
echo "   - Run tests: docker-compose -f docker-compose.fixed.yml exec web python test_app.py"
echo ""
echo "🔍 What was fixed:"
echo "   1. Changed from 'network_mode: host' to bridge networking"
echo "   2. Added 'extra_hosts' mapping for 192.168.91.110"
echo "   3. Used proper Docker network configuration"
echo ""
echo "📚 For more help, see: DOCKER_TROUBLESHOOTING.md" 