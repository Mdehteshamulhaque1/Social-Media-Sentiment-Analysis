# Production Docker Quick Reference Card

## 🚀 Quick Start Commands

### Windows
```powershell
# Setup
Copy-Item .env.example .env.production
notepad .env.production

# Deploy
.\deploy.bat

# Monitor
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f
```

### Linux / Mac
```bash
# Setup
cp .env.example .env.production
nano .env.production

# Deploy (Option 1: Auto)
chmod +x deploy.sh
./deploy.sh

# Deploy (Option 2: Make)
make build
make up

# Deploy (Option 3: Manual)
docker compose -f docker-compose.prod.yml up -d
```

---

## 🔧 Common Operations

| Task | Command |
|------|---------|
| **View Service Status** | `docker compose -f docker-compose.prod.yml ps` |
| **View Real-time Logs** | `docker compose -f docker-compose.prod.yml logs -f` |
| **View Service Logs Only** | `docker compose -f docker-compose.prod.yml logs fastapi` |
| **Stop Services** | `docker compose -f docker-compose.prod.yml down` |
| **Restart Service** | `docker compose -f docker-compose.prod.yml restart fastapi` |
| **Rebuild & Restart** | `docker compose -f docker-compose.prod.yml up -d --build fastapi` |
| **View Resource Usage** | `docker stats` |
| **Execute Command in Service** | `docker compose -f docker-compose.prod.yml exec fastapi bash` |

---

## 📊 Accessing Services

| Service | URL | Port |
|---------|-----|------|
| Frontend | http://localhost | 80 |
| API Docs | http://localhost/api/v1/docs | 80 |
| API ReDoc | http://localhost/api/v1/redoc | 80 |
| Django Admin | http://localhost:8001/admin | 8001 |
| FastAPI Direct | http://localhost:8000 | 8000 |
| PostgreSQL | localhost:5432 | 5432 |
| Redis | localhost:6379 | 6379 |

---

## 🗄️ Database Operations

```bash
# Backup Database
docker compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U sip_user sip_prod > backup.sql

# Restore Database
docker compose -f docker-compose.prod.yml exec postgres \
  psql -U sip_user sip_prod < backup.sql

# Connect to Database
docker compose -f docker-compose.prod.yml exec postgres \
  psql -U sip_user -d sip_prod

# Run Migrations
docker compose -f docker-compose.prod.yml exec django \
  python manage.py migrate

# Create Superuser
docker compose -f docker-compose.prod.yml exec django \
  python manage.py createsuperuser
```

---

## 🎯 Debugging Commands

```bash
# Check Service Health
docker compose -f docker-compose.prod.yml ps

# View Full Logs (last 100 lines)
docker compose -f docker-compose.prod.yml logs --tail=100

# Follow Specific Service Logs
docker compose -f docker-compose.prod.yml logs -f fastapi

# Check Network Connectivity
docker compose -f docker-compose.prod.yml exec fastapi \
  curl http://postgres:5432/

# Verify Redis Connection
docker compose -f docker-compose.prod.yml exec redis \
  redis-cli ping

# Database Connection Test
docker compose -f docker-compose.prod.yml exec fastapi \
  python -c "from backend.fastapi_service.app.db.session import SessionLocal; db = SessionLocal(); print('Connected!')"

# View Container Resource Usage
docker stats --no-stream

# Inspect Container
docker inspect sip_fastapi

# View Container Network
docker network inspect docker_compose_prod_sip_network
```

---

## 🔐 Security Checks

```bash
# Scan Docker Image for Vulnerabilities
docker scan sentiment-intelligence-fastapi:latest

# Verify No Root User in Container
docker compose -f docker-compose.prod.yml exec fastapi \
  id

# Check Environment Variables
docker compose -f docker-compose.prod.yml exec fastapi \
  env | grep -E 'POSTGRES|REDIS|DJANGO'

# Verify Secrets are Protected
grep -v "^#" .env.production | grep -v "^$" | head -5
```

---

## 📈 Performance Monitoring

```bash
# Monitor Real-time Resource Usage
docker stats

# Monitor Specific Service
docker stats sip_fastapi

# Check Database Connections
docker compose -f docker-compose.prod.yml exec postgres \
  psql -U sip_user -d sip_prod -c \
  "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"

# Check Redis Memory Usage
docker compose -f docker-compose.prod.yml exec redis \
  redis-cli info memory

# Check Celery Active Tasks
docker compose -f docker-compose.prod.yml exec fastapi \
  celery -A backend.fastapi_service.app.tasks.celery_app.celery_app inspect active

# View Slow Queries (requires PostgreSQL config)
docker compose -f docker-compose.prod.yml logs postgres | grep duration
```

---

## 🔄 Scaling Services

```bash
# Scale Celery Workers to 3 instances
docker compose -f docker-compose.prod.yml up -d --scale celery=3

# Scale FastAPI to 2 instances (requires load balancer)
docker compose -f docker-compose.prod.yml up -d --scale fastapi=2

# View Scaled Services
docker compose -f docker-compose.prod.yml ps
```

---

## ⚙️ Make Commands (Linux/Mac)

```bash
make help                   # Show all commands
make build                  # Build Docker images
make up                     # Start services
make down                   # Stop services
make logs                   # View all logs
make logs-fastapi          # View FastAPI logs
make restart-fastapi       # Restart FastAPI
make migrate               # Run migrations
make superuser             # Create admin user
make seed                  # Seed database
make backup-db             # Backup database
make restore-db FILE=...   # Restore database
make health-check          # Test all services
make stats                 # Show resource usage
make clean                 # Remove all (DESTRUCTIVE)
```

---

## 🚨 Troubleshooting Quick Fixes

### Services Won't Start
```bash
# View error logs
docker compose -f docker-compose.prod.yml logs

# Rebuild without cache
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d
```

### Out of Memory
```bash
# Check memory usage
docker stats

# Increase container memory in docker-compose.prod.yml:
#   deploy:
#     resources:
#       limits:
#         memory: 2G
```

### High CPU Usage
```bash
# Identify process
docker top sip_fastapi

# Reduce worker concurrency in docker-compose.prod.yml
```

### Database Connection Failed
```bash
# Check if PostgreSQL is running
docker compose -f docker-compose.prod.yml exec postgres \
  pg_isready -U sip_user -d sip_prod

# Check credentials in .env.production
grep POSTGRES .env.production
```

### Port Already in Use
```bash
# Find process using port
sudo lsof -i :80     # Linux/Mac
netstat -ano | findstr :80  # Windows

# Change port in docker-compose.prod.yml
# OR kill conflicting process
```

---

## 📝 Environment Variables - Key Reference

```bash
# Database
POSTGRES_DB=sip_prod
POSTGRES_USER=sip_user
POSTGRES_PASSWORD=<strong_password>

# Redis
REDIS_PASSWORD=<strong_password>

# Django
DJANGO_SECRET_KEY=<random_key>
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=yourdomain.com

# Service URLs
FASTAPI_BASE_URL=http://fastapi:8000/api/v1
VITE_API_BASE_URL=https://yourdomain.com/api/v1

# CORS
CORS_ORIGINS=https://yourdomain.com

# Environment
APP_ENV=production
LOG_LEVEL=info
```

---

## 🔗 File Structure Reference

```
Project Root
├── docker-compose.prod.yml       ← Use this for production
├── .env.production               ← Create and configure
├── backend/
│   ├── fastapi_service/
│   │   └── Dockerfile.prod       ← Production image
│   └── django_admin/
│       └── Dockerfile.prod       ← Production image
├── frontend/
│   └── Dockerfile.prod           ← Production image
├── infra/nginx/
│   ├── default.conf              ← Routing rules
│   ├── ssl/                      ← SSL certificates
│   │   ├── cert.pem
│   │   └── key.pem
├── logs/                         ← Service logs
│   ├── fastapi/
│   ├── django/
│   └── celery/
├── DOCKER_DEPLOYMENT_GUIDE.md    ← Full documentation
├── DOCKER_SECURITY_PERFORMANCE.md ← Security guide
├── deploy.sh                     ← Linux/Mac script
└── deploy.bat                    ← Windows script
```

---

## 📚 Documentation Files

- **DOCKER_SETUP_SUMMARY.md** - Quick overview and getting started
- **DOCKER_DEPLOYMENT_GUIDE.md** - Comprehensive deployment guide
- **DOCKER_SECURITY_PERFORMANCE.md** - Security and performance best practices
- **DEPLOYMENT_VERIFICATION_CHECKLIST.md** - Pre-deployment checklist
- **DOCKER_QUICK_REFERENCE.md** - This file

---

## 💡 Pro Tips

1. **Always backup before updates**
   ```bash
   make backup-db
   ```

2. **Check health before deploying**
   ```bash
   make health-check
   ```

3. **Use `-f` flag to ensure production config**
   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```

4. **Monitor logs during deployment**
   ```bash
   docker compose -f docker-compose.prod.yml logs -f
   ```

5. **Set up log rotation**
   - Configured in docker-compose.prod.yml
   - 10MB per file, max 5 files

6. **Use named volumes for persistence**
   - Data survives `docker compose down`
   - Backup named volumes for disaster recovery

7. **Test before going live**
   - Use `make health-check`
   - Run `docker stats` to monitor
   - Load test the API

8. **Keep images updated**
   ```bash
   docker compose -f docker-compose.prod.yml pull
   docker compose -f docker-compose.prod.yml up -d
   ```

---

**Last Updated:** May 10, 2024  
**Version:** 1.0.0
