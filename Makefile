# Production Makefile - Convenience commands for Docker operations

.PHONY: help build up down logs restart ps test backup restore clean migrate seed

# Variables
COMPOSE := docker compose -f docker-compose.prod.yml
ENV_FILE := .env.production
DOCKER_REGISTRY ?= myregistry
IMAGE_TAG ?= latest

## help: Display this help message
help:
	@sed -n 's/^##//p' $(MAKEFILE_LIST) | column -t -s ':' | sed -e 's/^/ /'

## build: Build all production Docker images
build:
	@echo "Building production images..."
	DOCKER_BUILDKIT=1 $(COMPOSE) build --progress=plain

## build-no-cache: Build all images without cache
build-no-cache:
	@echo "Building images (no cache)..."
	DOCKER_BUILDKIT=1 $(COMPOSE) build --no-cache --progress=plain

## up: Start all services in background
up:
	@echo "Starting services..."
	$(COMPOSE) up -d
	@echo "Waiting for services to be healthy..."
	@sleep 60
	@echo "Services started. Run 'make ps' to check status"

## down: Stop and remove all services
down:
	@echo "Stopping services..."
	$(COMPOSE) down

## down-volumes: Stop services and remove all volumes (DESTRUCTIVE)
down-volumes:
	@echo "WARNING: This will delete all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(COMPOSE) down -v; \
	fi

## ps: Show status of all services
ps:
	@$(COMPOSE) ps

## logs: View logs from all services (live)
logs:
	@$(COMPOSE) logs -f

## logs-fastapi: View FastAPI logs only
logs-fastapi:
	@$(COMPOSE) logs -f fastapi

## logs-django: View Django logs only
logs-django:
	@$(COMPOSE) logs -f django

## logs-celery: View Celery logs only
logs-celery:
	@$(COMPOSE) logs -f celery

## logs-postgres: View PostgreSQL logs only
logs-postgres:
	@$(COMPOSE) logs -f postgres

## restart: Restart all services
restart:
	@echo "Restarting services..."
	$(COMPOSE) restart
	@sleep 30
	@$(COMPOSE) ps

## restart-fastapi: Restart FastAPI service only
restart-fastapi:
	@$(COMPOSE) restart fastapi

## restart-django: Restart Django service only
restart-django:
	@$(COMPOSE) restart django

## restart-celery: Restart Celery service only
restart-celery:
	@$(COMPOSE) restart celery

## migrate: Run Django database migrations
migrate:
	@echo "Running migrations..."
	@$(COMPOSE) exec -T django python manage.py migrate

## makemigrations: Create new Django migrations
makemigrations:
	@$(COMPOSE) exec -T django python manage.py makemigrations

## superuser: Create Django superuser
superuser:
	@$(COMPOSE) exec django python manage.py createsuperuser

## seed: Seed database with sample data
seed:
	@echo "Seeding database..."
	@$(COMPOSE) exec -T fastapi python -m backend.fastapi_service.scripts.seed_data

## shell-django: Open Django management shell
shell-django:
	@$(COMPOSE) exec django python manage.py shell

## shell-postgres: Open PostgreSQL psql shell
shell-postgres:
	@$(COMPOSE) exec postgres psql -U sip_user -d sip_prod

## shell-redis: Open Redis CLI
shell-redis:
	@$(COMPOSE) exec redis redis-cli

## backup-db: Backup PostgreSQL database
backup-db:
	@echo "Backing up database..."
	@mkdir -p backups
	@$(COMPOSE) exec -T postgres pg_dump -U sip_user sip_prod > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup complete: backups/backup_$$(date +%Y%m%d_%H%M%S).sql"

## restore-db: Restore PostgreSQL database (specify FILE=path/to/backup.sql)
restore-db:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make restore-db FILE=backups/backup_YYYYMMDD_HHMMSS.sql"; \
		exit 1; \
	fi
	@echo "Restoring database from $(FILE)..."
	@$(COMPOSE) exec -T postgres psql -U sip_user sip_prod < $(FILE)
	@echo "Restore complete"

## backup-redis: Backup Redis data
backup-redis:
	@echo "Backing up Redis..."
	@mkdir -p backups
	@$(COMPOSE) exec -T redis redis-cli BGSAVE
	@echo "Redis backup triggered"

## stats: Show Docker resource usage statistics
stats:
	@docker stats --no-stream

## test: Run test suite
test:
	@echo "Running tests..."
	@$(COMPOSE) exec -T fastapi pytest
	@$(COMPOSE) exec -T django python manage.py test

## lint: Run linting on codebase
lint:
	@echo "Running linters..."
	@$(COMPOSE) exec -T fastapi ruff check .
	@$(COMPOSE) exec -T django ruff check .

## celery-inspect: Inspect active Celery tasks
celery-inspect:
	@$(COMPOSE) exec -T fastapi celery -A backend.fastapi_service.app.tasks.celery_app.celery_app inspect active

## celery-purge: Purge all Celery tasks (WARNING: Destructive)
celery-purge:
	@echo "WARNING: This will delete all pending tasks!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(COMPOSE) exec -T fastapi celery -A backend.fastapi_service.app.tasks.celery_app.celery_app purge; \
	fi

## db-size: Show database size
db-size:
	@$(COMPOSE) exec -T postgres psql -U sip_user -d sip_prod -c "SELECT pg_size_pretty(pg_database_size('sip_prod'))"

## db-connections: Show active database connections
db-connections:
	@$(COMPOSE) exec -T postgres psql -U sip_user -d sip_prod -c "SELECT datname, usename, count(*) FROM pg_stat_activity GROUP BY datname, usename"

## redis-memory: Show Redis memory usage
redis-memory:
	@$(COMPOSE) exec -T redis redis-cli info memory

## redis-keys: Show count of Redis keys
redis-keys:
	@$(COMPOSE) exec -T redis redis-cli DBSIZE

## health-check: Run all health checks
health-check:
	@echo "Checking PostgreSQL..."
	@$(COMPOSE) exec -T postgres pg_isready -U sip_user -d sip_prod && echo "✓ PostgreSQL OK" || echo "✗ PostgreSQL FAILED"
	@echo "Checking Redis..."
	@$(COMPOSE) exec -T redis redis-cli ping && echo "✓ Redis OK" || echo "✗ Redis FAILED"
	@echo "Checking FastAPI..."
	@$(COMPOSE) exec -T fastapi curl -s http://localhost:8000/api/v1/health | grep -q success && echo "✓ FastAPI OK" || echo "✗ FastAPI FAILED"
	@echo "All checks complete"

## push-images: Push Docker images to registry
push-images:
	@echo "Tagging images for $(DOCKER_REGISTRY)..."
	@docker tag sentiment-intelligence-fastapi $(DOCKER_REGISTRY)/sip-fastapi:$(IMAGE_TAG)
	@docker tag sentiment-intelligence-django $(DOCKER_REGISTRY)/sip-django:$(IMAGE_TAG)
	@docker tag sentiment-intelligence-frontend $(DOCKER_REGISTRY)/sip-frontend:$(IMAGE_TAG)
	@echo "Pushing to registry..."
	@docker push $(DOCKER_REGISTRY)/sip-fastapi:$(IMAGE_TAG)
	@docker push $(DOCKER_REGISTRY)/sip-django:$(IMAGE_TAG)
	@docker push $(DOCKER_REGISTRY)/sip-frontend:$(IMAGE_TAG)
	@echo "Push complete"

## clean: Remove all containers, images, and volumes (DESTRUCTIVE)
clean:
	@echo "WARNING: This will delete all containers and images!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(COMPOSE) down -v; \
		docker image prune -f; \
		echo "Clean complete"; \
	fi

## env-check: Verify environment configuration
env-check:
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "ERROR: $(ENV_FILE) not found"; \
		exit 1; \
	fi
	@echo "Environment file exists"
	@echo "Checking required variables:"
	@grep -q "POSTGRES_PASSWORD" $(ENV_FILE) && echo "✓ POSTGRES_PASSWORD" || echo "✗ POSTGRES_PASSWORD missing"
	@grep -q "DJANGO_SECRET_KEY" $(ENV_FILE) && echo "✓ DJANGO_SECRET_KEY" || echo "✗ DJANGO_SECRET_KEY missing"
	@grep -q "REDIS_PASSWORD" $(ENV_FILE) && echo "✓ REDIS_PASSWORD" || echo "✗ REDIS_PASSWORD missing"

## version: Show version information
version:
	@echo "Docker version:"
	@docker --version
	@echo "Docker Compose version:"
	@docker compose version
	@echo "Python version (in FastAPI):"
	@$(COMPOSE) exec -T fastapi python --version
