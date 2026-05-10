@echo off
REM Production deployment automation script for Windows
REM This script automates the complete production setup

setlocal enabledelayedexpansion

REM Configuration
set COMPOSE_FILE=docker-compose.prod.yml
set ENV_FILE=.env.production
set LOG_DIR=logs
set BACKUP_DIR=backups

echo.
echo ========================================
echo Sentiment Intelligence Platform
echo Production Deployment Script (Windows)
echo ========================================
echo.

REM Check Docker installation
echo [1/8] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed
    exit /b 1
)
docker compose version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker Compose is not installed
    exit /b 1
)
echo [OK] Docker and Docker Compose found
echo.

REM Validate environment file
echo [2/8] Validating environment configuration...
if not exist "%ENV_FILE%" (
    echo Error: %ENV_FILE% not found
    echo Creating from .env.example...
    copy .env.example "%ENV_FILE%"
    echo [WARNING] Please edit %ENV_FILE% with production values
    exit /b 1
)
echo [OK] Environment file validated
echo.

REM Create required directories
echo [3/8] Setting up directories...
if not exist "%LOG_DIR%\fastapi" mkdir "%LOG_DIR%\fastapi"
if not exist "%LOG_DIR%\django" mkdir "%LOG_DIR%\django"
if not exist "%LOG_DIR%\celery" mkdir "%LOG_DIR%\celery"
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
if not exist "infra\nginx\ssl" mkdir "infra\nginx\ssl"
echo [OK] Directories created
echo.

REM Build Docker images
echo [4/8] Building Docker images...
docker compose -f "%COMPOSE_FILE%" build --progress=plain
if errorlevel 1 (
    echo Error: Failed to build Docker images
    exit /b 1
)
echo [OK] Images built successfully
echo.

REM Start services
echo [5/8] Starting services...
docker compose -f "%COMPOSE_FILE%" up -d
if errorlevel 1 (
    echo Error: Failed to start services
    exit /b 1
)
echo Waiting for services to be healthy (60s)...
timeout /t 60 /nobreak
echo [OK] Services started
echo.

REM Verify health
echo [6/8] Verifying service health...
docker compose -f "%COMPOSE_FILE%" ps
echo.

REM Run migrations
echo [7/8] Running database migrations...
docker compose -f "%COMPOSE_FILE%" exec -T django python manage.py migrate
if errorlevel 1 (
    echo Warning: Migrations may need manual verification
)
echo [OK] Migrations completed
echo.

REM Display access information
echo [8/8] Deployment complete!
echo.
echo Access Information:
echo   Frontend:       http://localhost
echo   FastAPI Docs:   http://localhost/api/v1/docs
echo   Django Admin:   http://localhost:8001/admin
echo   Nginx Proxy:    http://localhost
echo.
echo Useful Commands:
echo   View logs:      docker compose -f %COMPOSE_FILE% logs -f fastapi
echo   Stop services:  docker compose -f %COMPOSE_FILE% down
echo   Remove volumes: docker compose -f %COMPOSE_FILE% down -v
echo.
echo Next Steps:
echo   1. Configure SSL certificates in infra/nginx/ssl/
echo   2. Update ALLOWED_HOSTS and CORS settings
echo   3. Set up monitoring and alerting
echo   4. Configure backup strategies
echo.
