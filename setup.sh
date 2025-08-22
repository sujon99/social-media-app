#!/bin/bash

echo "🚀 Social Media App Setup with Nginx"
echo "===================================="

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null

# Clean up
echo "🧹 Cleaning up..."
docker system prune -f

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs static nginx/ssl

# Generate SSL certificates
echo "🔐 Generating SSL certificates..."
if command -v openssl &> /dev/null; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/key.pem \
        -out nginx/ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" 2>/dev/null
    echo "✅ SSL certificates generated"
else
    echo "⚠️  OpenSSL not found. Please install OpenSSL or run generate-ssl.sh manually"
    echo "   Creating placeholder files..."
    touch nginx/ssl/key.pem nginx/ssl/cert.pem
fi

# Build and start
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting application with Nginx..."
docker-compose up -d

# Wait for startup
echo "⏳ Waiting for application to start..."
sleep 30

# Check status
echo "📊 Checking status..."
if docker ps | grep -q "social-media-app" && docker ps | grep -q "social-media-nginx"; then
    echo "✅ Application is running!"
    echo ""
    echo "🌐 Access your app at:"
    echo "   - HTTP: http://localhost (redirects to HTTPS)"
    echo "   - HTTPS: https://localhost"
    echo ""
    echo "📋 Useful commands:"
    echo "   - View logs: docker logs social-media-app"
    echo "   - View Nginx logs: docker logs social-media-nginx"
    echo "   - Stop app: docker-compose down"
    echo "   - Restart: docker-compose restart"
    echo ""
    echo "🔧 To create superuser:"
    echo "   docker exec social-media-app python manage.py createsuperuser"
    echo ""
    echo "🔧 To run tests:"
    echo "   docker exec social-media-app python test_app.py"
    echo ""
    echo "⚠️  Note: HTTPS uses self-signed certificate."
    echo "   Your browser will show a security warning."
else
    echo "❌ Application failed to start"
    echo "Checking logs..."
    docker logs social-media-app
    docker logs social-media-nginx
fi 