#!/bin/bash

echo "🚀 Setting up Social Media App with Nginx..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs static

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your server configuration before continuing!"
    echo "   Current settings use localhost - update with your actual server IPs."
    read -p "Press Enter after updating .env file..."
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "📊 Checking service status..."
docker-compose ps

echo "✅ Setup complete! Access at:"
echo "  - HTTP: http://localhost"
echo "  - HTTPS: https://localhost (redirects to HTTP)"
echo ""
echo "🔧 To customize for your server:"
echo "   1. Edit .env file with your server IPs"
echo "   2. Run: docker-compose down && docker-compose up -d"
echo ""
echo "📋 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop: docker-compose down"
echo "   - Restart: docker-compose restart"
echo ""
echo "🔐 To enable SSL later:"
echo "   1. Generate SSL certificates"
echo "   2. Uncomment SSL config in nginx/nginx.conf"
echo "   3. Add SSL volume mount to docker-compose.yml"
echo "   4. Restart: docker-compose restart" 