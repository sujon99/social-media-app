# 🚀 Social Media Application - Deployment Guide

This guide covers deploying the Django Social Media Application using Docker and Docker Compose.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB RAM available
- Ports 80, 443, 8000, 3306, 6379, 9000, 9001 available

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx (80/443)│    │  Django App     │    │   MySQL (3306)  │
│   (Reverse Proxy)│◄──►│   (8000)        │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Redis (6379)  │    │  MinIO (9000)   │
                       │   Cache         │    │  Object Storage │
                       └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd social-media-app

# Create necessary directories
mkdir -p logs static nginx/ssl mysql/init
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
# Django Settings
DJANGO_SETTINGS_MODULE=social_media.production
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Configuration
DATABASE_HOST=192.168.91.110
DATABASE_PORT=3306
DATABASE_NAME=mydb
DATABASE_USER=myuser
DATABASE_PASSWORD=mypassword

# Redis Configuration
REDIS_HOST=192.168.91.110
REDIS_PORT=6379

# MinIO Configuration
MINIO_ENDPOINT=192.168.91.110:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_BUCKET_NAME=social-media-app
MINIO_USE_HTTPS=false
```

### 3. SSL Certificates (Optional)

For production, place your SSL certificates in `nginx/ssl/`:

```bash
# Self-signed certificates for development
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx/ssl/key.pem \
    -out nginx/ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

### 4. Build and Deploy

```bash
# Build the application
docker-compose build

# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f web
```

## 🔧 Configuration Options

### Using External Services

If you want to use external services instead of the local containers:

```yaml
# Comment out or remove these services from docker-compose.yml
# mysql:
# redis:
# minio:
```

And update the environment variables in the `web` service to point to your external services.

### Production Settings

The Dockerfile automatically creates a production settings file with:

- Debug mode disabled
- Security headers enabled
- Static file collection
- Logging configuration
- Gunicorn WSGI server

## 📊 Monitoring and Health Checks

### Health Check Endpoints

- **Application**: `http://localhost:8000/health/`
- **Nginx**: `http://localhost/health/`

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs nginx
docker-compose logs mysql

# Follow logs in real-time
docker-compose logs -f web
```

### Performance Monitoring

```bash
# Check container resource usage
docker stats

# Check container health status
docker-compose ps
```

## 🔒 Security Features

### Built-in Security

- Non-root user execution
- Security headers (XSS, CSRF, HSTS)
- Rate limiting on API endpoints
- SSL/TLS encryption
- Content Security Policy

### Additional Security Measures

```bash
# Update secrets
docker-compose exec web python manage.py changepassword admin

# Review security settings
docker-compose exec web python manage.py check --deploy
```

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale the web service
docker-compose up -d --scale web=3

# Load balancer configuration needed for multiple instances
```

### Vertical Scaling

Update the `docker-compose.yml`:

```yaml
web:
  deploy:
    resources:
      limits:
        memory: 2G
        cpus: '1.0'
      reservations:
        memory: 1G
        cpus: '0.5'
```

## 🗄️ Database Management

### Backup

```bash
# Create database backup
docker-compose exec mysql mysqldump -u root -p mydb > backup.sql

# Restore database
docker-compose exec -T mysql mysql -u root -p mydb < backup.sql
```

### Migrations

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create new migrations
docker-compose exec web python manage.py makemigrations

# Show migration status
docker-compose exec web python manage.py showmigrations
```

## 🖼️ MinIO Management

### Access MinIO Console

- **URL**: `http://localhost:9001`
- **Username**: `minioadmin`
- **Password**: `minioadmin123`

### Bucket Operations

```bash
# List buckets
docker-compose exec minio mc ls

# Create bucket
docker-compose exec minio mc mb minio/social-media-app

# Set bucket policy
docker-compose exec minio mc policy set public minio/social-media-app
```

## 🧪 Testing

### Run Tests

```bash
# Run comprehensive test suite
docker-compose exec web python test_app.py

# Run Django tests
docker-compose exec web python manage.py test

# Check for security issues
docker-compose exec web python manage.py check --deploy
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Conflicts

```bash
# Check what's using the ports
netstat -tulpn | grep :8000
netstat -tulpn | grep :3306

# Kill conflicting processes
sudo kill -9 <PID>
```

#### 2. Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Fix Docker volume permissions
docker-compose down
sudo chown -R $USER:$USER logs static
docker-compose up -d
```

#### 3. Database Connection Issues

```bash
# Check database status
docker-compose exec mysql mysqladmin ping -u root -p

# Check Django database connection
docker-compose exec web python manage.py dbshell
```

#### 4. MinIO Connection Issues

```bash
# Check MinIO status
docker-compose exec minio mc admin info

# Test bucket access
docker-compose exec minio mc ls minio/social-media-app
```

### Debug Mode

For debugging, temporarily enable debug mode:

```bash
# Edit the production.py file in the container
docker-compose exec web sed -i 's/DEBUG = False/DEBUG = True/' social_media/production.py

# Restart the service
docker-compose restart web
```

## 📚 Additional Resources

### Useful Commands

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild and restart
docker-compose up -d --build

# View service logs
docker-compose logs -f [service-name]

# Execute commands in running container
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py createsuperuser
```

### Performance Tuning

```bash
# Optimize Django
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py compress

# Database optimization
docker-compose exec web python manage.py dbshell
# Run: ANALYZE TABLE users_user, posts_post, posts_comment;
```

## 🎯 Production Checklist

- [ ] SSL certificates configured
- [ ] Environment variables set
- [ ] Database backups scheduled
- [ ] Monitoring and alerting configured
- [ ] Log rotation configured
- [ ] Security headers verified
- [ ] Rate limiting tested
- [ ] Health checks working
- [ ] Performance benchmarks completed
- [ ] Disaster recovery plan tested

## 🆘 Support

For issues and questions:

1. Check the logs: `docker-compose logs -f`
2. Verify configuration: `docker-compose config`
3. Test individual components: `python test_app.py`
4. Check service health: `docker-compose ps`

---

**Happy Deploying! 🚀** 