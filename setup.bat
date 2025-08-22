@echo off
echo 🚀 Social Media App Setup with Nginx
echo ====================================

REM Stop any existing containers
echo 🛑 Stopping existing containers...
docker-compose down 2>nul

REM Clean up
echo 🧹 Cleaning up...
docker system prune -f

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "static" mkdir static
if not exist "nginx\ssl" mkdir nginx\ssl

REM Generate SSL certificates
echo 🔐 Generating SSL certificates...
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx\ssl\key.pem -out nginx\ssl\cert.pem -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" 2>nul
if %errorlevel% equ 0 (
    echo ✅ SSL certificates generated
) else (
    echo ⚠️  OpenSSL not found. Creating placeholder files...
    echo. > nginx\ssl\key.pem
    echo. > nginx\ssl\cert.pem
)

REM Build and start
echo 🔨 Building Docker images...
docker-compose build

echo 🚀 Starting application with Nginx...
docker-compose up -d

REM Wait for startup
echo ⏳ Waiting for application to start...
timeout /t 30 /nobreak >nul

REM Check status
echo 📊 Checking status...
docker ps | findstr "social-media-app" >nul
docker ps | findstr "social-media-nginx" >nul
if %errorlevel% equ 0 (
    echo ✅ Application is running!
    echo.
    echo 🌐 Access your app at:
    echo    - HTTP: http://localhost (redirects to HTTPS)
    echo    - HTTPS: https://localhost
    echo.
    echo 📋 Useful commands:
    echo    - View logs: docker logs social-media-app
    echo    - View Nginx logs: docker logs social-media-nginx
    echo    - Stop app: docker-compose down
    echo    - Restart: docker-compose restart
    echo.
    echo 🔧 To create superuser:
    echo    docker exec social-media-app python manage.py createsuperuser
    echo.
    echo 🔧 To run tests:
    echo    docker exec social-media-app python test_app.py
    echo.
    echo ⚠️  Note: HTTPS uses self-signed certificate.
    echo    Your browser will show a security warning.
) else (
    echo ❌ Application failed to start
    echo Checking logs...
    docker logs social-media-app
    docker logs social-media-nginx
)

echo.
echo Setup complete! 