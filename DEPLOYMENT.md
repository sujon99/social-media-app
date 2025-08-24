# 🚀 Deployment Guide

This guide explains how to deploy the Social Media Application on different types of servers and environments.

## 📋 Prerequisites

Before deploying, ensure you have:

- **Docker & Docker Compose** installed on your server
- **External services** running and accessible:
  - MySQL Database
  - Redis Server
  - MinIO Object Storage

## 🌐 Server Deployment Scenarios

### 1. Local Development Server

**Use Case**: Development and testing on your local machine

**Configuration**:
```bash
# Copy environment template
cp env.example .env

# Edit .env file
DATABASE_HOST=localhost
REDIS_HOST=localhost
MINIO_HOST=localhost
SERVER_HOST=localhost
```

**Deploy**:
```bash
# Linux/Mac
./setup.sh

# Windows
setup.bat
```

### 2. Single Server Deployment

**Use Case**: All services running on one server (192.168.1.100)

**Configuration**:
```bash
# Copy and edit environment file
cp env.example .env

# Update .env with your server IP
DATABASE_HOST=192.168.1.100
REDIS_HOST=192.168.1.100
MINIO_HOST=192.168.1.100
SERVER_HOST=192.168.1.100
```

**Deploy**:
```bash
./setup.sh
```

### 3. Multi-Server Deployment

**Use Case**: Services distributed across multiple servers

**Configuration**:
```bash
# Copy and edit environment file
cp env.example .env

# Update .env with different server IPs
DATABASE_HOST=192.168.1.10    # Database server
REDIS_HOST=192.168.1.20       # Redis server
MINIO_HOST=192.168.1.30       # Storage server
SERVER_HOST=192.168.1.100     # Application server
```

**Deploy**:
```bash
./setup.sh
```

### 4. Cloud Deployment (AWS/GCP/Azure)

**Use Case**: Deploying on cloud platforms

**Configuration**:
```bash
# Copy and edit environment file
cp env.example .env

# Update .env with cloud service endpoints
DATABASE_HOST=your-rds-endpoint.amazonaws.com
REDIS_HOST=your-elasticache-endpoint.amazonaws.com
MINIO_HOST=your-s3-endpoint.amazonaws.com
SERVER_HOST=your-app-domain.com
```

**Deploy**:
```bash
./setup.sh
```

### 5. Kubernetes Deployment

**Use Case**: Container orchestration with Kubernetes

**Configuration**:
```bash
# Use Kubernetes secrets for sensitive data
DATABASE_HOST=mysql-service
REDIS_HOST=redis-service
MINIO_HOST=minio-service
SERVER_HOST=your-app-domain.com
```

**Deploy**:
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

## 🔧 Environment Variables Reference

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `DATABASE_HOST` | MySQL server hostname/IP | `localhost`, `192.168.1.10`, `db.example.com` |
| `DATABASE_PORT` | MySQL server port | `3306` |
| `DATABASE_NAME` | Database name | `mydb`, `social_media` |
| `DATABASE_USER` | Database username | `myuser`, `admin` |
| `DATABASE_PASSWORD` | Database password | `mypassword`, `secure123` |
| `REDIS_HOST` | Redis server hostname/IP | `localhost`, `192.168.1.20`, `redis.example.com` |
| `REDIS_PORT` | Redis server port | `6379` |
| `MINIO_HOST` | MinIO server hostname/IP | `localhost`, `192.168.1.30`, `storage.example.com` |
| `MINIO_PORT` | MinIO server port | `9000` |
| `MINIO_ACCESS_KEY` | MinIO access key | `minioadmin`, `your-access-key` |
| `MINIO_SECRET_KEY` | MinIO secret key | `minioadmin123`, `your-secret-key` |
| `MINIO_BUCKET_NAME` | MinIO bucket name | `social-media-app`, `media-bucket` |
| `MINIO_USE_HTTPS` | Use HTTPS for MinIO | `true`, `false` |
| `SERVER_HOST` | Your server's public IP/domain | `localhost`, `192.168.1.100`, `app.example.com` |

## 🛠️ Service Setup

### MySQL Setup

```bash
# Install MySQL
sudo apt update
sudo apt install mysql-server

# Create database and user
mysql -u root -p
CREATE DATABASE mydb;
CREATE USER 'myuser'@'%' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'%';
FLUSH PRIVILEGES;
EXIT;

# Configure MySQL to accept external connections
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# Change bind-address = 127.0.0.1 to bind-address = 0.0.0.0

# Restart MySQL
sudo systemctl restart mysql
```

### Redis Setup

```bash
# Install Redis
sudo apt update
sudo apt install redis-server

# Configure Redis to accept external connections
sudo nano /etc/redis/redis.conf
# Change bind 127.0.0.1 to bind 0.0.0.0

# Restart Redis
sudo systemctl restart redis
```

### MinIO Setup

```bash
# Download MinIO
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio

# Create MinIO user
sudo useradd -r minio-user -s /sbin/nologin

# Create MinIO directory
sudo mkdir /opt/minio
sudo chown minio-user:minio-user /opt/minio

# Start MinIO
sudo -u minio-user ./minio server /opt/minio --address :9000

# Create bucket (via MinIO Console at http://your-server:9000)
# Login with minioadmin/minioadmin123
# Create bucket: social-media-app
```

## 🔒 Security Considerations

### Firewall Configuration

```bash
# Allow necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3306/tcp  # MySQL (if external)
sudo ufw allow 6379/tcp  # Redis (if external)
sudo ufw allow 9000/tcp  # MinIO (if external)

# Enable firewall
sudo ufw enable
```

### SSL/TLS Configuration

For production, replace self-signed certificates:

```bash
# Obtain certificates from Let's Encrypt
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to nginx/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem

# Restart application
docker-compose restart
```

## 📊 Monitoring and Logs

### View Application Logs

```bash
# Real-time logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f web
docker-compose logs -f nginx

# Historical logs
docker-compose logs --tail=100 web
```

### Health Checks

```bash
# Check service status
docker-compose ps

# Check application health
curl -I http://localhost/health/

# Check database connection
docker exec social-media-app python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT 1')
print('Database connection: OK')
"
```

## 🔄 Updates and Maintenance

### Application Updates

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d

# Run migrations
docker exec social-media-app python manage.py migrate
```

### Backup and Restore

```bash
# Database backup
docker exec social-media-app python manage.py dumpdata > backup.json

# Database restore
docker exec social-media-app python manage.py loaddata backup.json

# MinIO backup (if using local storage)
tar -czf minio-backup.tar.gz /opt/minio/
```

## 🚨 Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check if external services are running
   - Verify firewall settings
   - Check network connectivity

2. **CSRF Token Errors**
   - Verify `SERVER_HOST` in `.env`
   - Check if domain matches trusted origins

3. **Image Upload Failures**
   - Verify MinIO credentials
   - Check bucket permissions
   - Ensure bucket exists

4. **Session Issues**
   - Check Redis connectivity
   - Verify Redis configuration
   - Check session settings

### Debug Commands

```bash
# Test database connection
docker exec social-media-app python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT VERSION()')
print(cursor.fetchone())
"

# Test Redis connection
docker exec social-media-app python -c "
import redis
r = redis.Redis(host='$REDIS_HOST', port=$REDIS_PORT)
print('Redis connection:', r.ping())
"

# Test MinIO connection
docker exec social-media-app python -c "
from posts.utils import get_minio_client
client = get_minio_client()
buckets = client.list_buckets()
print('MinIO buckets:', [b.name for b in buckets])
"
```

## 📞 Support

For deployment issues:

1. Check the logs: `docker-compose logs -f`
2. Verify environment configuration
3. Test external service connectivity
4. Review firewall and network settings

---

**Happy Deploying! 🚀** 