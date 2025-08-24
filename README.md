# 🚀 Social Media Application

A modern Django-based social media application with Docker containerization, Nginx reverse proxy, and production-ready features.

## ✨ Features

- **User Authentication**: Signup, login, logout with secure session management
- **Post Management**: Create, edit, delete posts with image uploads
- **Profile Management**: Update profile information and profile pictures
- **Social Features**: Like posts, view other users' posts
- **High Availability**: Redis-based session storage for scalability
- **Object Storage**: MinIO integration for image storage
- **Production Ready**: Nginx reverse proxy with SSL/TLS support
- **Containerized**: Full Docker support for easy deployment

## 🏗️ Architecture

- **Frontend**: Django Templates with Bootstrap 5
- **Backend**: Django 4.2.7 with Python 3.11
- **Database**: MySQL 8.0
- **Cache/Sessions**: Redis
- **Object Storage**: MinIO
- **Web Server**: Nginx (reverse proxy) + Gunicorn (WSGI)
- **Containerization**: Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- MySQL server running
- Redis server running  
- MinIO server running

### 1. Clone and Setup

```bash
git clone <repository-url>
cd social-media-app
```

### 2. Configure Environment

Copy the environment template and customize it for your server:

```bash
cp env.example .env
```

Edit `.env` file with your server configuration:

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
SERVER_HOST=your-server-public-ip
```

### 3. Deploy

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
# Copy environment template
cp env.example .env

# Edit .env with your server configuration
notepad .env

# Build and start
docker-compose build
docker-compose up -d
```

### 4. Access Application

- **HTTP**: http://localhost
- **HTTPS**: https://localhost (redirects to HTTP)

## 🔧 Configuration

### Environment Variables

The application uses environment variables for all configuration. Key variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_HOST` | MySQL server IP | localhost |
| `REDIS_HOST` | Redis server IP | localhost |
| `MINIO_HOST` | MinIO server IP | localhost |
| `SERVER_HOST` | Your server's public IP | localhost |

### Port Configuration

- **Nginx**: 80 (HTTP), 443 (HTTPS)
- **Django**: 8000 (internal)
- **MySQL**: 3306
- **Redis**: 6379
- **MinIO**: 9000

## 📋 Management Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose down && docker-compose up -d --build
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
docker exec social-media-app python test_app.py
```

## 🔒 Security Features

- **CSRF Protection**: Enabled with dynamic trusted origins
- **Session Security**: Redis-based sessions with configurable timeouts
- **HTTPS**: Nginx SSL/TLS termination
- **Security Headers**: Implemented via Nginx
- **Input Validation**: Django form validation
- **SQL Injection Protection**: Django ORM

## 🌐 Deployment on Different Servers

The application is designed to be **server-agnostic**. To deploy on any server:

1. **Update `.env` file** with your server's IP addresses
2. **Ensure external services** (MySQL, Redis, MinIO) are accessible
3. **Run setup script** - it will automatically configure everything

### Example for Different Environments:

**Development (localhost):**
```bash
DATABASE_HOST=localhost
REDIS_HOST=localhost
MINIO_HOST=localhost
SERVER_HOST=localhost
```

**Production Server (192.168.1.100):**
```bash
DATABASE_HOST=192.168.1.100
REDIS_HOST=192.168.1.100
MINIO_HOST=192.168.1.100
SERVER_HOST=192.168.1.100
```

**Cloud Deployment (example.com):**
```bash
DATABASE_HOST=db.example.com
REDIS_HOST=redis.example.com
MINIO_HOST=storage.example.com
SERVER_HOST=app.example.com
```

## 🐛 Troubleshooting

### Common Issues

1. **Connection Refused**: Check if external services (MySQL, Redis, MinIO) are running
2. **CSRF Errors**: Verify `SERVER_HOST` in `.env` matches your server IP
3. **Image Upload Issues**: Ensure MinIO bucket exists and credentials are correct

### Logs

```bash
# Application logs
docker-compose logs web

# Nginx logs
docker-compose logs nginx

# All logs
docker-compose logs -f
```

## 📁 Project Structure

```
social-media-app/
├── social_media/          # Django project settings
├── users/                 # User management app
├── posts/                 # Post management app
├── templates/             # HTML templates
├── static/                # Static files
├── nginx/                 # Nginx configuration
├── logs/                  # Application logs
├── docker-compose.yml     # Docker services
├── Dockerfile            # Django application image
├── requirements.txt      # Python dependencies
├── env.example           # Environment template
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ using Django, Docker, and modern web technologies**

**Happy Social Media Building! 🚀** 