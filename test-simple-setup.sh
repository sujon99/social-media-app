#!/bin/bash

echo "🧪 Testing Simple Docker Setup"
echo "=============================="

# Test 1: Check if Docker is running
echo "1. Testing Docker availability..."
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running or not accessible"
    exit 1
fi
echo "✅ Docker is running"

# Test 2: Check if external services are reachable
echo "2. Testing external service connectivity..."
echo "   Testing MySQL (192.168.91.110:3306)..."
if timeout 5 bash -c '</dev/tcp/192.168.91.110/3306' 2>/dev/null; then
    echo "   ✅ MySQL is reachable"
else
    echo "   ❌ MySQL is NOT reachable"
fi

echo "   Testing Redis (192.168.91.110:6379)..."
if timeout 5 bash -c '</dev/tcp/192.168.91.110/6379' 2>/dev/null; then
    echo "   ✅ Redis is reachable"
else
    echo "   ❌ Redis is NOT reachable"
fi

echo "   Testing MinIO (192.168.91.110:9000)..."
if timeout 5 bash -c '</dev/tcp/192.168.91.110/9000' 2>/dev/null; then
    echo "   ✅ MinIO is reachable"
else
    echo "   ❌ MinIO is NOT reachable"
fi

# Test 3: Build the image
echo "3. Building Docker image..."
docker-compose -f docker-compose.simple.yml build

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Docker image build failed"
    exit 1
fi

# Test 4: Start the container
echo "4. Starting container..."
docker-compose -f docker-compose.simple.yml up -d

if [ $? -eq 0 ]; then
    echo "✅ Container started successfully"
else
    echo "❌ Container failed to start"
    exit 1
fi

# Test 5: Wait and check status
echo "5. Waiting for container to be ready..."
sleep 15

if docker ps | grep -q "social-media-app"; then
    echo "✅ Container is running"
else
    echo "❌ Container is not running"
    echo "Container logs:"
    docker logs social-media-app
    exit 1
fi

# Test 6: Test Django application
echo "6. Testing Django application..."
if curl -f http://localhost:8000/ >/dev/null 2>&1; then
    echo "✅ Django application is responding"
else
    echo "❌ Django application is not responding"
    echo "Container logs:"
    docker logs social-media-app
fi

echo ""
echo "🎉 All tests completed!"
echo ""
echo "📱 Your application is running at: http://localhost:8000"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: docker logs social-media-app"
echo "   - Stop: docker-compose -f docker-compose.simple.yml down"
echo "   - Restart: docker-compose -f docker-compose.simple.yml restart"
echo "   - Shell: docker exec -it social-media-app bash" 