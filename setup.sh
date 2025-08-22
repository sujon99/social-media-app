#!/bin/bash

echo "🚀 Social Media App Setup"
echo "========================"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null

# Clean up
echo "🧹 Cleaning up..."
docker system prune -f

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p logs

# Build and start
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting application..."
docker-compose up -d

# Wait for startup
echo "⏳ Waiting for application to start..."
sleep 20

# Check status
echo "📊 Checking status..."
if docker ps | grep -q "social-media-app"; then
    echo "✅ Application is running!"
    echo ""
    echo "🌐 Access your app at: http://localhost:8000"
    echo ""
    echo "📋 Useful commands:"
    echo "   - View logs: docker logs social-media-app"
    echo "   - Stop app: docker-compose down"
    echo "   - Restart: docker-compose restart"
    echo ""
    echo "🔧 To create superuser:"
    echo "   docker exec social-media-app python manage.py createsuperuser"
    echo ""
    echo "🔧 To run tests:"
    echo "   docker exec social-media-app python test_app.py"
else
    echo "❌ Application failed to start"
    echo "Checking logs..."
    docker logs social-media-app
fi 