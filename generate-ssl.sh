#!/bin/bash

echo "🔐 Generating SSL Certificates for Nginx"
echo "========================================"

# Create SSL directory
echo "📁 Creating SSL directory..."
mkdir -p nginx/ssl

# Generate self-signed certificate
echo "🔑 Generating self-signed SSL certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx/ssl/key.pem \
    -out nginx/ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

if [ $? -eq 0 ]; then
    echo "✅ SSL certificate generated successfully!"
    echo "📁 Certificate location: nginx/ssl/"
    echo "   - cert.pem (certificate)"
    echo "   - key.pem (private key)"
else
    echo "❌ Failed to generate SSL certificate"
    echo "Please install OpenSSL or generate certificates manually"
    exit 1
fi

echo ""
echo "🔒 SSL setup complete!"
echo "Your application will be available at:"
echo "   - HTTP: http://localhost (redirects to HTTPS)"
echo "   - HTTPS: https://localhost"
echo ""
echo "⚠️  Note: This is a self-signed certificate."
echo "   Your browser will show a security warning."
echo "   For production, use a proper SSL certificate." 