#!/bin/bash

echo "🔍 Diagnosing Docker Container Connectivity Issues"
echo "================================================"

# Check if container is running
if ! docker ps | grep -q "social-media-app"; then
    echo "❌ Container 'social-media-app' is not running"
    echo "Starting container for diagnosis..."
    docker-compose -f docker-compose.simple.yml up -d
    sleep 10
fi

echo "✅ Container is running"
echo ""

# Test network connectivity from inside the container
echo "🌐 Testing Network Connectivity from Container:"
echo "----------------------------------------------"

echo "1. Testing basic network connectivity..."
docker exec social-media-app ping -c 3 192.168.91.110

echo ""
echo "2. Testing MySQL port connectivity..."
docker exec social-media-app bash -c "timeout 5 bash -c '</dev/tcp/192.168.91.110/3306' && echo '✅ MySQL port 3306 is accessible' || echo '❌ MySQL port 3306 is NOT accessible'"

echo ""
echo "3. Testing Redis port connectivity..."
docker exec social-media-app bash -c "timeout 5 bash -c '</dev/tcp/192.168.91.110/6379' && echo '✅ Redis port 6379 is accessible' || echo '❌ Redis port 6379 is NOT accessible'"

echo ""
echo "4. Testing MinIO port connectivity..."
docker exec social-media-app bash -c "timeout 5 bash -c '</dev/tcp/192.168.91.110/9000' && echo '✅ MinIO port 9000 is accessible' || echo '❌ MinIO port 9000 is NOT accessible'"

echo ""
echo "5. Testing from host machine..."
echo "Testing MySQL from host:"
timeout 5 bash -c '</dev/tcp/192.168.91.110/3306' && echo '✅ Host can reach MySQL' || echo '❌ Host cannot reach MySQL'

echo ""
echo "6. Container network configuration:"
docker inspect social-media-app | grep -A 10 "NetworkSettings"

echo ""
echo "7. Container logs (last 20 lines):"
docker logs --tail 20 social-media-app

echo ""
echo "🔧 Quick Fixes to Try:"
echo "======================"
echo "1. If container can't reach external services, try:"
echo "   docker-compose -f docker-compose.simple.yml down"
echo "   docker run --rm -it --network host -e DATABASE_HOST=192.168.91.110 social-media-app_web"
echo ""
echo "2. If host can't reach external services, check:"
echo "   - Firewall settings"
echo "   - Network configuration"
echo "   - Service status on 192.168.91.110"
echo ""
echo "3. Alternative: Use bridge network with extra hosts:"
echo "   Add to docker-compose.simple.yml:"
echo "   extra_hosts:"
echo "     - '192.168.91.110:host-gateway'"
echo "   # Remove network_mode: host" 