# 🐳 Docker Troubleshooting Guide

This guide helps resolve common Docker issues when running the Social Media Application.

## 🚨 Common Issues & Solutions

### 1. **Container Stuck After "Starting application..."**

**Problem**: Container appears to hang after collecting static files and starting Gunicorn.

**Root Cause**: Usually a network connectivity issue to external services (MySQL, Redis, MinIO).

**Solutions**:

#### **Option A: Check Environment Configuration**
```bash
# Verify your .env file exists and is configured
cat .env

# Ensure all required variables are set
DATABASE_HOST=your-mysql-server-ip
REDIS_HOST=your-redis-server-ip
MINIO_HOST=your-minio-server-ip
SERVER_HOST=your-server-ip
```

#### **Option B: Test External Service Connectivity**
```bash
# Test connectivity from your host machine (replace with your IPs)
telnet $DATABASE_HOST 3306  # MySQL
telnet $REDIS_HOST 6379     # Redis
telnet $MINIO_HOST 9000     # MinIO

# If these fail, check your network configuration
```

#### **Option C: Use Bridge Network with Extra Hosts**
```bash
# Add this to your docker-compose.yml if needed
extra_hosts:
  - "${DATABASE_HOST}:host-gateway"
  - "${REDIS_HOST}:host-gateway"
  - "${MINIO_HOST}:host-gateway"
```

### 2. **Database Connection Timeout**

**Problem**: Container fails with database connection timeout.

**Solutions**:

```bash
# Check if your external MySQL is accessible
mysql -h $DATABASE_HOST -u $DATABASE_USER -p $DATABASE_NAME

# Verify credentials in .env file
DATABASE_HOST=your-mysql-server-ip
DATABASE_USER=myuser
DATABASE_PASSWORD=mypassword
DATABASE_NAME=mydb

# Test from within container
docker exec -it social-media-app bash
python manage.py check --database default
```

### 3. **Redis Connection Issues**

**Problem**: Container can't connect to Redis.

**Solutions**:

```bash
# Test Redis connectivity
redis-cli -h $REDIS_HOST -p $REDIS_PORT ping

# Check Redis configuration
redis-cli -h $REDIS_HOST -p $REDIS_PORT config get bind
redis-cli -h $REDIS_HOST -p $REDIS_PORT config get protected-mode
```

### 4. **MinIO Connection Issues**

**Problem**: Container can't connect to MinIO.

**Solutions**:

```bash
# Test MinIO connectivity
curl -I http://$MINIO_HOST:$MINIO_PORT

# Check MinIO console
curl -I http://$MINIO_HOST:9001

# Verify credentials
curl -u $MINIO_ACCESS_KEY:$MINIO_SECRET_KEY http://$MINIO_HOST:$MINIO_PORT
```

## 🔧 Quick Fix Commands

### **Reset Everything**
```bash
# Stop all containers
docker-compose down

# Remove all containers and images
docker system prune -a -f

# Rebuild from scratch
docker-compose build
docker-compose up -d
```

### **Check Container Status**
```bash
# View running containers
docker ps

# View container logs
docker logs social-media-app

# View container details
docker inspect social-media-app
```

### **Network Diagnostics**
```bash
# Check container network
docker network ls
docker network inspect social-media-app_social-media-network

# Test network connectivity from container
docker exec -it social-media-app bash
ping $DATABASE_HOST
telnet $DATABASE_HOST 3306
```

## 🚀 Recommended Setup

### **For External Services**
```bash
# 1. Copy environment template
cp env.example .env

# 2. Edit .env with your server IPs
nano .env

# 3. Run setup
./setup.sh
```

### **For Local Development (All Services in Docker)**
```bash
# Configure for localhost
DATABASE_HOST=localhost
REDIS_HOST=localhost
MINIO_HOST=localhost
SERVER_HOST=localhost

# Run setup
./setup.sh
```

## 📋 Troubleshooting Checklist

- [ ] **Environment File**: Does `.env` file exist and contain correct IPs?
- [ ] **External Services Accessible**: Can you connect to your service IPs from host?
- [ ] **Ports Open**: Are ports 3306, 6379, 9000 accessible?
- [ ] **Credentials Correct**: Are the database/Redis/MinIO credentials correct?
- [ ] **Network Mode**: Are you using the right network configuration?
- [ ] **Container Logs**: Have you checked the container logs for errors?
- [ ] **Service Dependencies**: Are external services running and healthy?

## 🆘 Emergency Commands

### **Force Stop Everything**
```bash
# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -aq)

# Clean up volumes
docker volume prune -f
```

### **Quick Test**
```bash
# Test if your external services are working
python test_app.py

# If this works, the issue is with Docker networking
# If this fails, the issue is with your external services
```

### **Manual Container Run**
```bash
# Run container manually to see what happens
docker run --rm -it \
  -p 8000:8000 \
  --network host \
  -e DATABASE_HOST=$DATABASE_HOST \
  -e REDIS_HOST=$REDIS_HOST \
  -e MINIO_HOST=$MINIO_HOST \
  social-media-app_web
```

## 🔍 Debug Mode

### **Enable Debug in Container**
```bash
# Enter container
docker exec -it social-media-app bash

# Check environment variables
env | grep -E "(DATABASE|REDIS|MINIO)"

# Check Django settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES)
>>> print(settings.CACHES)
>>> print(settings.MINIO_ENDPOINT)
```

### **Check Django Settings**
```bash
# Verify settings are loaded correctly
docker exec -it social-media-app python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES)
>>> print(settings.CACHES)
>>> print(settings.MINIO_ENDPOINT)
```

## 📞 Getting Help

If you're still having issues:

1. **Check the logs**: `docker logs social-media-app`
2. **Verify environment**: Check your `.env` file configuration
3. **Test connectivity**: Test connectivity to your service IPs
4. **Check network**: Ensure no firewall/network restrictions
5. **Verify credentials**: Double-check database/Redis/MinIO credentials

## 🔧 Environment Variables Reference

Make sure your `.env` file contains all required variables:

```bash
# Database Configuration
DATABASE_HOST=your-mysql-server-ip
DATABASE_PORT=3306
DATABASE_NAME=mydb
DATABASE_USER=myuser
DATABASE_PASSWORD=mypassword

# Redis Configuration
REDIS_HOST=your-redis-server-ip
REDIS_PORT=6379

# MinIO Configuration
MINIO_HOST=your-minio-server-ip
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_BUCKET_NAME=social-media-app

# Server Configuration
SERVER_HOST=your-server-ip
```

---

**Remember**: Always check your `.env` file first - most issues are related to incorrect environment configuration! 