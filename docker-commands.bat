@echo off
REM Social Media Application - Docker Commands for Windows
REM Common commands for development and deployment

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="build" goto build
if "%1"=="up" goto up
if "%1"=="down" goto down
if "%1"=="logs" goto logs
if "%1"=="test" goto test
if "%1"=="setup" goto setup
if "%1"=="setup-simple" goto setup-simple
if "%1"=="build-simple" goto build-simple
if "%1"=="up-simple" goto up-simple
if "%1"=="down-simple" goto down-simple
if "%1"=="migrate" goto migrate
if "%1"=="collectstatic" goto collectstatic
if "%1"=="createsuperuser" goto createsuperuser
if "%1"=="shell" goto shell
if "%1"=="clean" goto clean
goto help

:help
echo Social Media Application - Available Commands:
echo.
echo Development:
echo   build          - Build Docker images
echo   up             - Start all services
echo   down           - Stop all services
echo   logs           - View logs for all services
echo.
echo Simple Setup (External Services):
echo   setup-simple   - Setup with external services
echo   build-simple   - Build web service only
echo   up-simple      - Start web service only
echo   down-simple    - Stop web service only
echo.
echo Django Management:
echo   shell          - Open Django shell
echo   migrate        - Run database migrations
echo   collectstatic  - Collect static files
echo   createsuperuser - Create superuser
echo   test           - Run comprehensive test suite
echo.
echo Maintenance:
echo   clean          - Remove containers, images, and volumes
echo.
echo Usage: docker-commands.bat [command]
echo Example: docker-commands.bat setup-simple
goto end

:setup
echo Setting up Social Media Application for first time...
if not exist "logs" mkdir logs
if not exist "static" mkdir static
if not exist "nginx\ssl" mkdir nginx\ssl
if not exist "mysql\init" mkdir mysql\init
echo Building and starting services...
call :build
call :up
echo Waiting for services to start...
timeout /t 30 /nobreak >nul
echo Running initial setup...
call :migrate
call :collectstatic
echo Setup complete! Access the application at:
echo   - Application: http://localhost:8000
echo   - Nginx: http://localhost
echo   - MinIO Console: http://localhost:9001
echo   - Create superuser: docker-commands.bat createsuperuser
goto end

:setup-simple
echo Setting up Social Media Application with external services...
if not exist "logs" mkdir logs
if not exist "static" mkdir static
echo Building and starting web service...
call :build-simple
call :up-simple
echo Waiting for service to start...
timeout /t 20 /nobreak >nul
echo Running initial setup...
call :migrate
call :collectstatic
echo Setup complete! Access the application at:
echo   - Application: http://localhost:8000
echo   - Create superuser: docker-commands.bat createsuperuser
goto end

:build
echo Building Docker images...
docker-compose build
goto end

:build-simple
echo Building web service...
docker-compose -f docker-compose.simple.yml build
goto end

:up
echo Starting all services...
docker-compose up -d
goto end

:up-simple
echo Starting web service...
docker-compose -f docker-compose.simple.yml up -d
goto end

:down
echo Stopping all services...
docker-compose down
goto end

:down-simple
echo Stopping web service...
docker-compose -f docker-compose.simple.yml down
goto end

:logs
echo Viewing logs for all services...
docker-compose logs -f
goto end

:test
echo Running comprehensive test suite...
docker-compose exec web python test_app.py
goto end

:migrate
echo Running database migrations...
docker-compose exec web python manage.py migrate
goto end

:collectstatic
echo Collecting static files...
docker-compose exec web python manage.py collectstatic --noinput
goto end

:createsuperuser
echo Creating superuser...
docker-compose exec web python manage.py createsuperuser
goto end

:shell
echo Opening Django shell...
docker-compose exec web python manage.py shell
goto end

:clean
echo Cleaning up Docker resources...
docker-compose down -v --rmi all
docker system prune -f
goto end

:end
echo.
echo Command completed. 