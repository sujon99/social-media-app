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
- **Security**: CSRF protection, secure headers, SSL/TLS encryption

### 🐳 Containerization
- **Docker Support**: Complete containerization with Docker Compose
- **Nginx Reverse Proxy**: Production-ready with SSL/TLS support
- **Gunicorn WSGI**: High-performance application server
- **Automatic Setup**: Database checking, migrations, and static file collection

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
- OpenSSL (for SSL certificate generation)
- External services running on 192.168.91.110:
  - MySQL (port 3306)
  - Redis (port 6379)
  - MinIO (port 9000)

### 1. Clone Repository
```bash
git clone https://github.com/sujon99/social-media-app.git
cd social-media-app
```

### 2. Quick Setup (Recommended)
```bash
# Using Makefile (Linux/Mac)
make setup

# Using Windows batch file
setup.bat

# Using shell script (Linux)
chmod +x setup.sh
./setup.sh

# Manual Docker commands
docker-compose build
docker-compose up -d
```

### 3. Access Application
- **HTTP**: http://localhost (redirects to HTTPS)
- **HTTPS**: https://localhost

## 🔧 Configuration

### Environment Variables
The application automatically uses these environment variables from docker-compose.yml:

```env
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
```

## 📋 Management Commands

### Using Makefile (Linux/Mac)
```bash
make help          # Show all available commands
make build         # Build Docker images
make up            # Start application
make down          # Stop application
make logs          # View logs
make logs-web      # View web logs
make logs-nginx    # View Nginx logs
make restart       # Restart application
make setup         # Complete setup (build + start)
make clean         # Clean up Docker resources
make ssl           # Generate SSL certificates
```

### Using Docker Compose
```bash
# Build and start
docker-compose build
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs -f web
docker-compose logs -f nginx

# Stop
docker-compose down

# Restart
docker-compose restart
```

### Django Management
```bash
# Open Django shell
docker exec social-media-app python manage.py shell

# Run migrations
docker exec social-media-app python manage.py migrate

# Collect static files
docker exec social-media-app python manage.py collectstatic

# Create superuser
docker exec social-media-app python manage.py createsuperuser

# Run tests
docker exec social-media-app python test_app.py
```

## 🧪 Testing

### Run Test Suite
```bash
# Using Makefile
make test

# Using Docker
docker exec social-media-app python test_app.py
```

The test suite covers:
- Database connectivity
- Redis operations
- MinIO file operations
- Django models and views
- Session management
- High availability features

## 🔒 SSL Configuration

### Self-Signed Certificates
The setup automatically generates self-signed SSL certificates:
- **Location**: `nginx/ssl/`
- **Files**: `cert.pem` (certificate), `key.pem` (private key)
- **Validity**: 365 days

### Production SSL
For production deployment, replace the self-signed certificates:
1. Obtain SSL certificates from a trusted CA
2. Replace `nginx/ssl/cert.pem` and `nginx/ssl/key.pem`
3. Restart the application: `docker-compose restart`

## 🔍 Troubleshooting

### Common Issues
1. **Database Connection**: Ensure MySQL is running on 192.168.91.110:3306
2. **Redis Connection**: Ensure Redis is running on 192.168.91.110:6379
3. **MinIO Connection**: Ensure MinIO is running on 192.168.91.110:9000
4. **SSL Certificate**: Check if certificates exist in `nginx/ssl/`

### Check Logs
```bash
# View application logs
docker logs social-media-app

# View Nginx logs
docker logs social-media-nginx

# View real-time logs
docker logs -f social-media-app
docker logs -f social-media-nginx
```

### Reset Everything
```bash
# Clean up and restart
make clean
make setup
```

## 📁 Project Structure

```
social-media-app/
├── social_media/          # Django project settings
├── users/                 # User management app
├── posts/                 # Post management app
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS)
├── logs/                  # Application logs
├── nginx/                 # Nginx configuration
│   ├── nginx.conf        # Nginx configuration
│   └── ssl/              # SSL certificates
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker services configuration
├── requirements.txt       # Python dependencies
├── setup.sh              # Linux setup script
├── setup.bat             # Windows setup script
├── generate-ssl.sh       # SSL certificate generation
├── Makefile              # Development commands
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using Django, Docker, and modern web technologies**

**Happy Social Media Building! 🚀** 