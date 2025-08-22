# 🐳 Docker Troubleshooting Guide

This guide helps resolve common Docker issues when running the Social Media Application.

## 🚨 Common Issues & Solutions

### 1. **Container Stuck After "Starting application..."**

**Problem**: Container appears to hang after collecting static files and starting Gunicorn.

**Root Cause**: Usually a network connectivity issue to external services (MySQL, Redis, MinIO).

**Solutions**:

#### **Option A: Use Host Network Mode (Recommended)**
```bash
# Use the simplified docker-compose file
docker-compose -f docker-compose.simple.yml up -d

# Or use the Makefile
make setup-simple
```

#### **Option B: Check External Service Connectivity**
```bash
# Test connectivity from your host machine
telnet 192.168.91.110 3306  # MySQL
telnet 192.168.91.110 6379  # Redis
telnet 192.168.91.110 9000  # MinIO

# If these fail, check your network configuration
```

#### **Option C: Use Bridge Network with Extra Hosts**
```bash
# Add this to your docker-compose.yml
extra_hosts:
  - "192.168.91.110:host-gateway"
```

### 2. **Database Connection Timeout**

**Problem**: Container fails with database connection timeout.

**Solutions**:

```bash
# Check if your external MySQL is accessible
mysql -h 192.168.91.110 -u myuser -p mydb

# Verify credentials in docker-compose.yml
environment:
  - DATABASE_HOST=192.168.91.110
  - DATABASE_USER=myuser
  - DATABASE_PASSWORD=mypassword
  - DATABASE_NAME=mydb

# Test from within container
docker exec -it social-media-app bash
python manage.py check --database default
```

### 3. **Redis Connection Issues**

**Problem**: Container can't connect to Redis.

**Solutions**:

```bash
# Test Redis connectivity
redis-cli -h 192.168.91.110 -p 6379 ping

# Check Redis configuration
redis-cli -h 192.168.91.110 -p 6379 config get bind
redis-cli -h 192.168.91.110 -p 6379 config get protected-mode
```

### 4. **MinIO Connection Issues**

**Problem**: Container can't connect to MinIO.

**Solutions**:

```bash
# Test MinIO connectivity
curl -I http://192.168.91.110:9000

# Check MinIO console
curl -I http://192.168.91.110:9001

# Verify credentials
curl -u minioadmin:minioadmin123 http://192.168.91.110:9000
```

## 🔧 Quick Fix Commands

### **Reset Everything**
```bash
# Stop all containers
docker-compose down
docker-compose -f docker-compose.simple.yml down

# Remove all containers and images
docker system prune -a -f

# Rebuild from scratch
make build-simple
make up-simple
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
ping 192.168.91.110
telnet 192.168.91.110 3306
```

## 🚀 Recommended Setup

### **For External Services (Your Current Setup)**
```bash
# Use the simplified setup
make setup-simple

# This will:
# 1. Build only the web service
# 2. Connect to your existing services on 192.168.91.110
# 3. Avoid network conflicts
```

### **For Local Development (All Services in Docker)**
```bash
# Use the full setup (if you want everything local)
make setup

# This will:
# 1. Start MySQL, Redis, MinIO containers
# 2. Start the web service
# 3. Configure internal networking
```

## 📋 Troubleshooting Checklist

- [ ] **External Services Accessible**: Can you connect to 192.168.91.110 from your host?
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
  -e DATABASE_HOST=192.168.91.110 \
  -e REDIS_HOST=192.168.91.110 \
  -e MINIO_ENDPOINT=192.168.91.110:9000 \
  social-media-app_web
```

## 🔍 Debug Mode

### **Enable Debug in Container**
```bash
# Enter container
docker exec -it social-media-app bash

# Edit production settings
sed -i 's/DEBUG = False/DEBUG = True/' social_media/production.py

# Restart container
docker restart social-media-app

# Check logs
docker logs -f social-media-app
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
2. **Verify external services**: Test connectivity to 192.168.91.110
3. **Use simple setup**: `make setup-simple`
4. **Check network**: Ensure no firewall/network restrictions
5. **Verify credentials**: Double-check database/Redis/MinIO credentials

---

**Remember**: The simplified setup (`make setup-simple`) is designed specifically for your external services configuration and should work without network conflicts. 