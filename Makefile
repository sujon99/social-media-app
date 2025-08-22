# Social Media Application - Makefile
# Common commands for development and deployment

.PHONY: help build up down logs test clean restart shell migrate collectstatic

# Default target
help:
	@echo "Social Media Application - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  build          - Build Docker images"
	@echo "  up             - Start all services"
	@echo "  down           - Stop all services"
	@echo "  restart        - Restart all services"
	@echo "  logs           - View logs for all services"
	@echo "  logs-web       - View logs for web service only"
	@echo ""
	@echo "Django Management:"
	@echo "  shell          - Open Django shell"
	@echo "  migrate        - Run database migrations"
	@echo "  collectstatic  - Collect static files"
	@echo "  createsuperuser - Create superuser"
	@echo "  test           - Run comprehensive test suite"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean          - Remove containers, images, and volumes"
	@echo "  backup         - Create database backup"
	@echo "  restore        - Restore database from backup"
	@echo ""

# Build Docker images
build:
	@echo "Building Docker images..."
	docker-compose build

# Start all services
up:
	@echo "Starting all services..."
	docker-compose up -d

# Stop all services
down:
	@echo "Stopping all services..."
	docker-compose down

# Restart all services
restart:
	@echo "Restarting all services..."
	docker-compose restart

# View logs for all services
logs:
	@echo "Viewing logs for all services..."
	docker-compose logs -f

# View logs for web service only
logs-web:
	@echo "Viewing logs for web service..."
	docker-compose logs -f web

# Open Django shell
shell:
	@echo "Opening Django shell..."
	docker-compose exec web python manage.py shell

# Run database migrations
migrate:
	@echo "Running database migrations..."
	docker-compose exec web python manage.py migrate

# Collect static files
collectstatic:
	@echo "Collecting static files..."
	docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
createsuperuser:
	@echo "Creating superuser..."
	docker-compose exec web python manage.py createsuperuser

# Run comprehensive test suite
test:
	@echo "Running comprehensive test suite..."
	docker-compose exec web python test_app.py

# Clean up containers, images, and volumes
clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v --rmi all
	docker system prune -f

# Create database backup
backup:
	@echo "Creating database backup..."
	@mkdir -p backups
	docker-compose exec mysql mysqldump -u root -prootpassword mydb > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup created in backups/ directory"

# Restore database from backup
restore:
	@if [ -z "$(file)" ]; then \
		echo "Usage: make restore file=backups/backup_filename.sql"; \
		exit 1; \
	fi
	@echo "Restoring database from $(file)..."
	docker-compose exec -T mysql mysql -u root -prootpassword mydb < $(file)

# Show service status
status:
	@echo "Service status:"
	docker-compose ps

# Show resource usage
stats:
	@echo "Resource usage:"
	docker stats --no-stream

# Health check
health:
	@echo "Health check:"
	@curl -f http://localhost:8000/ || echo "Application not responding"
	@curl -f http://localhost/health/ || echo "Nginx not responding"

# Development mode (with debug enabled)
dev:
	@echo "Starting development mode..."
	docker-compose exec web sed -i 's/DEBUG = False/DEBUG = True/' social_media/production.py
	docker-compose restart web

# Production mode (with debug disabled)
prod:
	@echo "Starting production mode..."
	docker-compose exec web sed -i 's/DEBUG = True/DEBUG = False/' social_media/production.py
	docker-compose restart web

# Quick setup for first time
setup:
	@echo "Setting up Social Media Application for first time..."
	@mkdir -p logs static nginx/ssl
	@echo "Building and starting web service..."
	@make build-simple
	@make up-simple
	@echo "Waiting for service to start..."
	@sleep 20
	@echo "Running initial setup..."
	@make migrate-simple
	@make collectstatic-simple
	@echo "Setup complete! Access the application at:"
	@echo "  - Application: http://localhost:8000"
	@echo "  - Create superuser: make createsuperuser-simple"

# Simple setup (external services)
setup-simple:
	@echo "Setting up Social Media Application with external services..."
	@mkdir -p logs static
	@echo "Building and starting web service..."
	@make build-simple
	@make up-simple
	@echo "Waiting for service to start..."
	@sleep 20
	@echo "Running initial setup..."
	@make migrate-simple
	@make collectstatic-simple
	@echo "Setup complete! Access the application at:"
	@echo "  - Application: http://localhost:8000"
	@echo "  - Create superuser: make createsuperuser-simple"

# Build simple (web only)
build-simple:
	@echo "Building web service..."
	docker-compose -f docker-compose.simple.yml build

# Start simple (web only)
up-simple:
	@echo "Starting web service..."
	docker-compose -f docker-compose.simple.yml up -d

# Stop simple (web only)
down-simple:
	@echo "Stopping web service..."
	docker-compose -f docker-compose.simple.yml down

# Django management for simple setup
shell-simple:
	@echo "Opening Django shell..."
	docker-compose -f docker-compose.simple.yml exec web python manage.py shell

migrate-simple:
	@echo "Running database migrations..."
	docker-compose -f docker-compose.simple.yml exec web python manage.py migrate

collectstatic-simple:
	@echo "Collecting static files..."
	docker-compose -f docker-compose.simple.yml exec web python manage.py collectstatic --noinput

createsuperuser-simple:
	@echo "Creating superuser..."
	docker-compose -f docker-compose.simple.yml exec web python manage.py createsuperuser

test-simple:
	@echo "Running comprehensive test suite..."
	docker-compose -f docker-compose.simple.yml exec web python test_app.py

logs-simple:
	@echo "Viewing web service logs..."
	docker-compose -f docker-compose.simple.yml logs -f web 