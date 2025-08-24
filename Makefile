# Social Media Application Makefile

.PHONY: help build up down logs restart clean test setup

help: ## Show this help message
	@echo "Social Media Application - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker-compose build

up: ## Start the application
	docker-compose up -d

down: ## Stop the application
	docker-compose down

logs: ## View application logs
	docker-compose logs -f

logs-web: ## View web application logs
	docker-compose logs -f web

logs-nginx: ## View Nginx logs
	docker-compose logs -f nginx

restart: ## Restart the application
	docker-compose restart

clean: ## Clean up Docker resources
	docker-compose down
	docker system prune -f

test: ## Run comprehensive test suite
	python test_app.py

setup: ## Complete setup (build + start)
	@echo "🚀 Setting up Social Media App..."
	@echo "📁 Creating directories..."
	@mkdir -p logs static
	@echo "🔨 Building Docker images..."
	@docker-compose build
	@echo "🚀 Starting services..."
	@docker-compose up -d
	@echo "⏳ Waiting for services to start..."
	@sleep 10
	@echo "📊 Checking service status..."
	@docker-compose ps
	@echo ""
	@echo "✅ Setup complete! Access at:"
	@echo "  - HTTP: http://localhost"
	@echo ""
	@echo "📋 Useful commands:"
	@echo "   - View logs: make logs"
	@echo "   - Stop: make down"
	@echo "   - Restart: make restart"
	@echo "   - Run tests: make test" 