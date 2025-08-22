# 🚀 Social Media Application

A modern, scalable social media platform built with Django, featuring user authentication, post management, image storage, and high availability architecture.

## ✨ Features

### 🔐 User Management
- **User Registration & Authentication**: Secure signup/login with email verification
- **Profile Management**: Update profile information, change passwords, upload profile pictures
- **Session Management**: Redis-backed sessions for high availability

### 📝 Content Management
- **Post Creation**: Create posts with images, titles, and descriptions
- **Image Storage**: MinIO object storage for scalable image management
- **Like & Comment System**: Interactive social features
- **Search Functionality**: Search posts by title, content, or author

### 🏗️ Architecture
- **High Availability**: Redis session storage enables multi-node deployment
- **Scalable Storage**: MinIO object storage for media files
- **Modern UI**: Bootstrap 5 with responsive design
- **Security**: CSRF protection, secure headers, rate limiting

### 🐳 Containerization
- **Docker Support**: Complete containerization with Docker Compose
- **Production Ready**: Gunicorn WSGI server with Nginx reverse proxy
- **Health Checks**: Built-in health monitoring and logging

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MySQL 8.0
- **Cache**: Redis 6.0+
- **Object Storage**: MinIO
- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Frontend**: Bootstrap 5, Font Awesome
- **Containerization**: Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB+ RAM available
- Ports 80, 443, 8000, 3306, 6379, 9000, 9001 available

### 1. Clone Repository
```bash
git clone https://github.com/sujon99/social-media-app.git
cd social-media-app
```

### 2. Quick Setup (Recommended)
```bash
# One-command setup
make setup
```

### 3. Manual Setup
```bash
# Create necessary directories
mkdir -p logs static nginx/ssl mysql/init

# Build and start services
make build
make up

# Run initial setup
make migrate
make collectstatic
```

### 4. Access Application
- **Main App**: http://localhost:8000
- **Nginx**: http://localhost
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin123)

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
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

### Using External Services
If you have existing MySQL, Redis, or MinIO services:

1. Comment out the corresponding services in `docker-compose.yml`
2. Update environment variables to point to your external services
3. Ensure network connectivity between containers and external services

## 📊 Management Commands

### Using Makefile (Recommended)
```bash
# View all available commands
make help

# Development
make up          # Start services
make down        # Stop services
make logs        # View logs
make restart     # Restart services

# Django Management
make migrate     # Run migrations
make shell       # Open Django shell
make test        # Run test suite
make backup      # Create database backup

# Maintenance
make clean       # Clean up Docker resources
make health      # Health check
```

### Using Docker Compose Directly
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Execute commands
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py migrate
```

## 🧪 Testing

### Run Comprehensive Test Suite
```bash
# Using Makefile
make test

# Direct execution
python test_app.py
```

### Test Coverage
The test suite covers:
- ✅ Redis connection and operations
- ✅ MinIO upload/download/delete operations
- ✅ Django models and relationships
- ✅ Redis session management
- ✅ URL configuration and routing
- ✅ Django forms validation
- ✅ High availability features

## 🐳 Docker Architecture

### Multi-Stage Build
- **Stage 1**: Build dependencies and create virtual environment
- **Stage 2**: Production runtime with minimal footprint

### Services
- **web**: Django application with Gunicorn
- **mysql**: MySQL 8.0 database
- **redis**: Redis cache server
- **minio**: MinIO object storage
- **nginx**: Reverse proxy with SSL support

### Volumes
- **mysql_data**: Persistent database storage
- **redis_data**: Persistent cache storage
- **minio_data**: Persistent object storage
- **logs**: Application logs
- **static**: Static files

## 🔒 Security Features

### Built-in Security
- Non-root user execution
- Security headers (XSS, CSRF, HSTS)
- Rate limiting on API endpoints
- SSL/TLS encryption
- Content Security Policy

### Production Hardening
- Debug mode disabled
- Secure cookie settings
- Database connection security
- File upload validation

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale web service
docker-compose up -d --scale web=3

# Load balancer configuration needed
```

### Vertical Scaling
Update `docker-compose.yml`:
```yaml
web:
  deploy:
    resources:
      limits:
        memory: 2G
        cpus: '1.0'
```

## 🗄️ Database Management

### Backup
```bash
# Create backup
make backup

# Restore backup
make restore file=backups/backup_20231201_120000.sql
```

### Migrations
```bash
# Run migrations
make migrate

# Create migrations
docker-compose exec web python manage.py makemigrations
```

## 🖼️ MinIO Management

### Access Console
- **URL**: http://localhost:9001
- **Username**: minioadmin
- **Password**: minioadmin123

### Bucket Operations
```bash
# List buckets
docker-compose exec minio mc ls

# Create bucket
docker-compose exec minio mc mb minio/social-media-app
```

## 🚨 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check port usage
netstat -tulpn | grep :8000

# Kill conflicting processes
sudo kill -9 <PID>
```

#### Permission Issues
```bash
# Fix permissions
sudo chown -R $USER:$USER .

# Fix Docker volume permissions
make down
sudo chown -R $USER:$USER logs static
make up
```

#### Database Issues
```bash
# Check database status
docker-compose exec mysql mysqladmin ping -u root -p

# Check Django connection
docker-compose exec web python manage.py dbshell
```

### Debug Mode
```bash
# Enable debug mode
make dev

# Disable debug mode
make prod
```

## 📚 API Endpoints

### Authentication
- `POST /login/` - User login
- `POST /signup/` - User registration
- `POST /logout/` - User logout

### Posts
- `GET /posts/` - List all posts
- `POST /posts/create/` - Create new post
- `GET /posts/<id>/` - View post details
- `PUT /posts/<id>/edit/` - Edit post
- `DELETE /posts/<id>/delete/` - Delete post
- `POST /posts/<id>/like/` - Like/unlike post

### Profile
- `GET /profile/` - View/edit profile
- `POST /profile/` - Update profile
- `GET /change-password/` - Change password

## 🔄 Development Workflow

### 1. Local Development
```bash
# Start development server
python manage.py runserver

# Run tests
python test_app.py

# Make changes and test
```

### 2. Docker Development
```bash
# Start services
make up

# View logs
make logs-web

# Make changes and rebuild
make build
make restart
```

### 3. Production Deployment
```bash
# Build production image
make build

# Deploy with production settings
make up

# Monitor health
make health
```

## 📋 Production Checklist

- [ ] SSL certificates configured
- [ ] Environment variables set
- [ ] Database backups scheduled
- [ ] Monitoring configured
- [ ] Log rotation configured
- [ ] Security headers verified
- [ ] Rate limiting tested
- [ ] Health checks working
- [ ] Performance benchmarks completed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
1. Check the logs: `make logs`
2. Verify configuration: `docker-compose config`
3. Run tests: `make test`
4. Check service health: `make health`

### Documentation
- [Deployment Guide](DEPLOYMENT.md) - Detailed deployment instructions
- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)

---

**Built with ❤️ using Django, Docker, and modern web technologies**

**Happy Social Media Building! 🚀** 