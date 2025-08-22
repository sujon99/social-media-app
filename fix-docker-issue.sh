#!/bin/bash

echo "🔧 Fixing Docker Networking Issue for Social Media App"
echo "=================================================="

# Check if we're on Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✅ Linux detected - proceeding with fix"
else
    echo "❌ This script is for Linux systems"
    echo "For Windows, use: docker-commands.bat setup-simple"
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null
docker-compose -f docker-compose.simple.yml down 2>/dev/null

# Clean up any hanging containers
echo "🧹 Cleaning up Docker resources..."
docker system prune -f

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs static

# Test external service connectivity
echo "🔍 Testing external service connectivity..."
echo "Testing MySQL connection to 192.168.91.110:3306..."
if timeout 5 bash -c "</dev/tcp/192.168.91.110/3306" 2>/dev/null; then
    echo "✅ MySQL connection successful"
else
    echo "❌ MySQL connection failed - check your network configuration"
    echo "Make sure 192.168.91.110 is accessible from this machine"
    exit 1
fi

echo "Testing Redis connection to 192.168.91.110:6379..."
if timeout 5 bash -c "</dev/tcp/192.168.91.110/6379" 2>/dev/null; then
    echo "✅ Redis connection successful"
else
    echo "❌ Redis connection failed - check your network configuration"
    exit 1
fi

echo "Testing MinIO connection to 192.168.91.110:9000..."
if timeout 5 bash -c "</dev/tcp/192.168.91.110/9000" 2>/dev/null; then
    echo "✅ MinIO connection successful"
else
    echo "❌ MinIO connection failed - check your network configuration"
    exit 1
fi

# Build the web service
echo "🔨 Building web service..."
docker-compose -f docker-compose.simple.yml build

if [ $? -ne 0 ]; then
    echo "❌ Build failed - check the error messages above"
    exit 1
fi

# Start the web service
echo "🚀 Starting web service..."
docker-compose -f docker-compose.simple.yml up -d

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
    docker-compose -f docker-compose.simple.yml logs web
    exit 1
fi

# Run migrations
echo "🗄️ Running database migrations..."
docker-compose -f docker-compose.simple.yml exec web python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ Migrations failed - check the error messages above"
    exit 1
fi

# Collect static files
echo "📁 Collecting static files..."
docker-compose -f docker-compose.simple.yml exec web python manage.py collectstatic --noinput

if [ $? -ne 0 ]; then
    echo "❌ Static file collection failed - check the error messages above"
    exit 1
fi

echo ""
echo "🎉 Setup Complete! Your Social Media App is now running."
echo ""
echo "📱 Access your application at:"
echo "   - Main App: http://localhost:8000"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: docker-compose -f docker-compose.simple.yml logs -f web"
echo "   - Stop service: docker-compose -f docker-compose.simple.yml down"
echo "   - Create superuser: docker-compose -f docker-compose.simple.yml exec web python manage.py createsuperuser"
echo "   - Run tests: docker-compose -f docker-compose.simple.yml exec web python test_app.py"
echo ""
echo "🚨 If you still have issues, check:"
echo "   1. Network connectivity to 192.168.91.110"
echo "   2. Service credentials (MySQL, Redis, MinIO)"
echo "   3. Container logs: docker logs social-media-app"
echo ""
echo "📚 For more help, see: DOCKER_TROUBLESHOOTING.md" 