#!/bin/bash

echo "🌐 Testing Application Accessibility"
echo "=================================="

# Get the server IP from environment or use localhost
SERVER_IP=${SERVER_HOST:-localhost}

echo "📊 Server Configuration:"
echo "   Server IP: $SERVER_IP"
echo "   Port: 80"
echo ""

# Test local access
echo "🔍 Testing local access..."
if curl -f -s http://localhost/ >/dev/null 2>&1; then
    echo "✅ Local access (localhost) - OK"
else
    echo "❌ Local access (localhost) - FAILED"
fi

# Test server IP access
echo "🔍 Testing server IP access..."
if curl -f -s http://$SERVER_IP/ >/dev/null 2>&1; then
    echo "✅ Server IP access ($SERVER_IP) - OK"
else
    echo "❌ Server IP access ($SERVER_IP) - FAILED"
fi

# Test external access (if different from localhost)
if [ "$SERVER_IP" != "localhost" ]; then
    echo "🔍 Testing external access..."
    if curl -f -s http://$SERVER_IP/ >/dev/null 2>&1; then
        echo "✅ External access ($SERVER_IP) - OK"
    else
        echo "❌ External access ($SERVER_IP) - FAILED"
        echo "   This might be due to firewall or network configuration"
    fi
fi

# Test with different Host headers
echo ""
echo "🔍 Testing with different Host headers..."
echo "   Testing with 'example.com' Host header..."
if curl -f -s -H "Host: example.com" http://$SERVER_IP/ >/dev/null 2>&1; then
    echo "✅ Custom Host header (example.com) - OK"
else
    echo "❌ Custom Host header (example.com) - FAILED"
fi

echo "   Testing with 'myapp.local' Host header..."
if curl -f -s -H "Host: myapp.local" http://$SERVER_IP/ >/dev/null 2>&1; then
    echo "✅ Custom Host header (myapp.local) - OK"
else
    echo "❌ Custom Host header (myapp.local) - FAILED"
fi

# Check container status
echo ""
echo "📊 Container Status:"
docker-compose ps

# Check nginx logs
echo ""
echo "📋 Recent Nginx Logs:"
docker-compose logs --tail=10 nginx

echo ""
echo "🎯 Application should now be accessible from:"
echo "   - http://localhost"
echo "   - http://$SERVER_IP"
echo "   - Any domain pointing to $SERVER_IP"
echo ""
echo "🔧 To test with custom domains:"
echo "   1. Add to /etc/hosts:"
echo "      192.168.91.110 myapp.local"
echo "      192.168.91.110 example.com"
echo "   2. Access: http://myapp.local or http://example.com"
