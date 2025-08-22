@echo off
echo 🚀 Simple Social Media App Setup
echo ================================

REM Stop any existing containers
echo 🛑 Stopping existing containers...
docker-compose -f docker-compose.simple.yml down 2>nul

REM Clean up
echo 🧹 Cleaning up...
docker system prune -f

REM Create logs directory
echo 📁 Creating logs directory...
if not exist "logs" mkdir logs

REM Build and start
echo 🔨 Building simple Docker image...
docker-compose -f docker-compose.simple.yml build

echo 🚀 Starting application...
docker-compose -f docker-compose.simple.yml up -d

REM Wait a bit
echo ⏳ Waiting for application to start...
timeout /t 10 /nobreak >nul

REM Check status
echo 📊 Checking status...
docker ps | findstr "social-media-app" >nul
if %errorlevel% equ 0 (
    echo ✅ Application is running!
    echo.
    echo 🌐 Access your app at: http://localhost:8000
    echo.
    echo 📋 Useful commands:
    echo    - View logs: docker logs social-media-app
    echo    - Stop app: docker-compose -f docker-compose.simple.yml down
    echo    - Restart: docker-compose -f docker-compose.simple.yml restart
    echo.
    echo 🔧 To run migrations:
    echo    docker exec social-media-app python manage.py migrate
    echo.
    echo 🔧 To create superuser:
    echo    docker exec social-media-app python manage.py createsuperuser
) else (
    echo ❌ Application failed to start
    echo Checking logs...
    docker logs social-media-app
)

echo.
echo Setup complete! 