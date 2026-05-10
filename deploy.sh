#!/bin/bash
# Production deployment automation script
# This script automates the complete production setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.production"
LOG_DIR="logs"
BACKUP_DIR="backups"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Sentiment Intelligence Platform${NC}"
echo -e "${GREEN}Production Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}\n"

# Function to check if Docker is installed
check_docker() {
    echo -e "${YELLOW}[1/8] Checking Docker installation...${NC}"
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        exit 1
    fi
    if ! command -v docker compose &> /dev/null; then
        echo -e "${RED}Error: Docker Compose is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker and Docker Compose found${NC}\n"
}

# Function to validate environment file
validate_env() {
    echo -e "${YELLOW}[2/8] Validating environment configuration...${NC}"
    
    if [ ! -f "$ENV_FILE" ]; then
        echo -e "${RED}Error: $ENV_FILE not found${NC}"
        echo -e "${YELLOW}Creating from .env.example...${NC}"
        cp .env.example "$ENV_FILE"
        echo -e "${RED}⚠ Please edit $ENV_FILE with production values${NC}"
        exit 1
    fi
    
    # Check critical variables
    if ! grep -q "POSTGRES_PASSWORD" "$ENV_FILE"; then
        echo -e "${RED}Error: POSTGRES_PASSWORD not set in $ENV_FILE${NC}"
        exit 1
    fi
    
    if ! grep -q "DJANGO_SECRET_KEY" "$ENV_FILE" || grep -q "change_me" "$ENV_FILE"; then
        echo -e "${RED}Error: DJANGO_SECRET_KEY not properly configured${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Environment file validated${NC}\n"
}

# Function to create required directories
setup_directories() {
    echo -e "${YELLOW}[3/8] Setting up directories...${NC}"
    mkdir -p "$LOG_DIR"/fastapi
    mkdir -p "$LOG_DIR"/django
    mkdir -p "$LOG_DIR"/celery
    mkdir -p "$BACKUP_DIR"
    mkdir -p "infra/nginx/ssl"
    echo -e "${GREEN}✓ Directories created${NC}\n"
}

# Function to build Docker images
build_images() {
    echo -e "${YELLOW}[4/8] Building Docker images...${NC}"
    docker compose -f "$COMPOSE_FILE" build --progress=plain
    echo -e "${GREEN}✓ Images built successfully${NC}\n"
}

# Function to start services
start_services() {
    echo -e "${YELLOW}[5/8] Starting services...${NC}"
    docker compose -f "$COMPOSE_FILE" up -d
    
    # Wait for services to be healthy
    echo -e "${YELLOW}Waiting for services to be healthy (60s)...${NC}"
    sleep 60
    
    echo -e "${GREEN}✓ Services started${NC}\n"
}

# Function to verify health
verify_health() {
    echo -e "${YELLOW}[6/8] Verifying service health...${NC}"
    
    echo "Service Status:"
    docker compose -f "$COMPOSE_FILE" ps
    
    # Check individual health
    if docker compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U sip_user &> /dev/null; then
        echo -e "${GREEN}✓ PostgreSQL healthy${NC}"
    else
        echo -e "${RED}✗ PostgreSQL unhealthy${NC}"
    fi
    
    if docker compose -f "$COMPOSE_FILE" exec -T redis redis-cli ping &> /dev/null; then
        echo -e "${GREEN}✓ Redis healthy${NC}"
    else
        echo -e "${RED}✗ Redis unhealthy${NC}"
    fi
    
    echo ""
}

# Function to run migrations
run_migrations() {
    echo -e "${YELLOW}[7/8] Running database migrations...${NC}"
    docker compose -f "$COMPOSE_FILE" exec -T django python manage.py migrate
    echo -e "${GREEN}✓ Migrations completed${NC}\n"
}

# Function to display access information
show_access_info() {
    echo -e "${YELLOW}[8/8] Deployment complete!${NC}\n"
    
    echo -e "${GREEN}Access Information:${NC}"
    echo -e "  ${YELLOW}Frontend:${NC}       http://localhost"
    echo -e "  ${YELLOW}FastAPI Docs:${NC}   http://localhost/api/v1/docs"
    echo -e "  ${YELLOW}Django Admin:${NC}   http://localhost:8001/admin"
    echo -e "  ${YELLOW}Nginx Proxy:${NC}    http://localhost\n"
    
    echo -e "${GREEN}Useful Commands:${NC}"
    echo -e "  View logs:        docker compose -f $COMPOSE_FILE logs -f fastapi"
    echo -e "  Scale workers:    docker compose -f $COMPOSE_FILE up -d --scale celery=3"
    echo -e "  Database backup:  docker compose -f $COMPOSE_FILE exec postgres pg_dump -U sip_user sip_prod > backup.sql"
    echo -e "  Stop services:    docker compose -f $COMPOSE_FILE down"
    echo -e "  Remove volumes:   docker compose -f $COMPOSE_FILE down -v\n"
    
    echo -e "${YELLOW}Next Steps:${NC}"
    echo -e "  1. Configure SSL certificates in infra/nginx/ssl/"
    echo -e "  2. Update ALLOWED_HOSTS and CORS settings"
    echo -e "  3. Set up monitoring and alerting"
    echo -e "  4. Configure backup strategies"
    echo -e "  5. Review DOCKER_DEPLOYMENT_GUIDE.md for advanced setup\n"
}

# Main execution
main() {
    check_docker
    validate_env
    setup_directories
    build_images
    start_services
    verify_health
    run_migrations
    show_access_info
}

# Run main function
main
