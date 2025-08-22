# Social Media Application - Makefile
# Simple commands for development and deployment

.PHONY: help build up down logs test clean restart shell migrate collectstatic createsuperuser ssl

# Default target
help:
	@echo "Social Media Application - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  build          - Build Docker images"
	@echo "  up             - Start application"
	@echo "  down           - Stop application"
	@echo "  restart        - Restart application"
	@echo "  logs           - View logs"
	@echo "  logs-web       - View web logs"
	@echo "  logs-nginx     - View Nginx logs"
	@echo ""
	@echo "Django Management:"
	@echo "  shell          - Open Django shell"
	@echo "  migrate        - Run database migrations"
	@echo "  collectstatic  - Collect static files"
	@echo "  createsuperuser - Create superuser"
	@echo "  test           - Run test suite"
	@echo ""
	@echo "SSL & Security:"
	@echo "  ssl            - Generate SSL certificates"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean          - Remove containers and images"
	@echo "  setup          - Complete setup (build + start)"

# Build Docker image
build:
	@echo "Building Docker images..."
	docker-compose build

# Start application
up:
	@echo "Starting application..."
	docker-compose up -d

# Stop application
down:
	@echo "Stopping application..."
	docker-compose down

# Restart application
restart:
	@echo "Restarting application..."
	docker-compose restart

# View logs
logs:
	@echo "Viewing logs..."
	docker-compose logs -f

# View web logs
logs-web:
	@echo "Viewing web logs..."
	docker-compose logs -f web

# View Nginx logs
logs-nginx:
	@echo "Viewing Nginx logs..."
	docker-compose logs -f nginx

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

# Run test suite
test:
	@echo "Running test suite..."
	docker-compose exec web python test_app.py

# Generate SSL certificates
ssl:
	@echo "Generating SSL certificates..."
	@mkdir -p nginx/ssl
	@openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout nginx/ssl/key.pem \
		-out nginx/ssl/cert.pem \
		-subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" 2>/dev/null || \
		echo "SSL certificate generation failed. Please install OpenSSL or run generate-ssl.sh manually"
	@echo "SSL certificates generated in nginx/ssl/"

# Clean up containers and images
clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v --rmi all
	docker system prune -f

# Complete setup
setup:
	@echo "Setting up Social Media Application..."
	@mkdir -p logs static nginx/ssl
	@make ssl
	@make build
	@make up
	@echo "Waiting for application to start..."
	@sleep 30
	@echo "Setup complete! Access at:"
	@echo "  - HTTP: http://localhost (redirects to HTTPS)"
	@echo "  - HTTPS: https://localhost" 