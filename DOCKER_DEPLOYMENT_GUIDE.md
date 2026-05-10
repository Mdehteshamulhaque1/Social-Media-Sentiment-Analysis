# Production Docker Setup Guide
## Sentiment Intelligence Platform

This document provides comprehensive guidance for deploying the Sentiment Intelligence Platform using Docker Compose in a production environment.

---

## Quick Start

```bash
# 1. Create production environment file
cp .env.example .env.production

# 2. Edit with production credentials
nano .env.production

# 3. Build and start services
docker compose -f docker-compose.prod.yml up -d

# 4. Verify all services are healthy
docker compose -f docker-compose.prod.yml ps
```

---

## Architecture Overview

### Services

| Service | Port | Purpose |
|---------|------|---------|
| **PostgreSQL** | 5432 | Primary database |
| **Redis** | 6379 | Caching & Celery broker |
| **FastAPI** | 8000 | Analytics API & WebSockets |
| **Celery** | — | Background job worker |
| **Django** | 8001 | Auth, RBAC, Admin panel |
| **Frontend** | 3000 | React dashboard (via Nginx) |
| **Nginx** | 80/443 | Reverse proxy & load balancer |

### Data Flow
```
User Browser → Nginx (80/443) → Frontend (React)
                          ↓
                    FastAPI (8000) → PostgreSQL
                          ↓
                    WebSocket Updates
                    
Celery Tasks ← Redis ← FastAPI/Django
         ↓
    PostgreSQL
```

---

## File Structure

```
.
├── docker-compose.prod.yml      # Production orchestration
├── .env.example                 # Environment template
├── backend/
│   ├── fastapi_service/
│   │   └── Dockerfile.prod      # FastAPI production image
│   └── django_admin/
│       └── Dockerfile.prod      # Django production image
├── frontend/
│   └── Dockerfile.prod          # Frontend production image
├── infra/nginx/
│   ├── default.conf             # Nginx routing
│   └── ssl/                     # SSL certificates (optional)
└── .dockerignore.enhanced       # Docker build exclusions
```

---

## Environment Configuration

### Production .env File

Create `.env.production` with these critical variables:

```bash
# Database
POSTGRES_DB=sip_prod
POSTGRES_USER=sip_user
POSTGRES_PASSWORD=<strong_random_password>

# Redis
REDIS_PASSWORD=<strong_random_password>

# Django
DJANGO_SECRET_KEY=<generate_with_python_secrets>
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
APP_ENV=production

# CORS
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
CORS_ORIGIN_REGEX=https://.*\.yourdomain\.com

# Service URLs
FASTAPI_BASE_URL=http://fastapi:8000/api/v1
VITE_API_BASE_URL=https://yourdomain.com/api/v1

# Logging
LOG_LEVEL=info
```

### Generate Django Secret Key

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Building Production Images

### Option 1: Build Locally
```bash
docker compose -f docker-compose.prod.yml build --no-cache
```

### Option 2: Build with BuildKit (faster, better caching)
```bash
DOCKER_BUILDKIT=1 docker compose -f docker-compose.prod.yml build --progress=plain
```

### Option 3: Use Docker Hub Registry
```bash
# Tag images
docker tag sentiment-intelligence-fastapi myregistry/sip-fastapi:latest
docker tag sentiment-intelligence-django myregistry/sip-django:latest
docker tag sentiment-intelligence-frontend myregistry/sip-frontend:latest

# Push to registry
docker push myregistry/sip-fastapi:latest
docker push myregistry/sip-django:latest
docker push myregistry/sip-frontend:latest
```

---

## Deployment

### First-Time Setup

```bash
# 1. Create required directories
mkdir -p logs/fastapi logs/celery logs/django infra/nginx/ssl

# 2. Start services
docker compose -f docker-compose.prod.yml up -d

# 3. Monitor startup (wait ~60 seconds)
docker compose -f docker-compose.prod.yml logs -f

# 4. Initialize database (if needed)
docker compose -f docker-compose.prod.yml exec django \
  python manage.py migrate

# 5. Create superuser (if needed)
docker compose -f docker-compose.prod.yml exec django \
  python manage.py createsuperuser

# 6. Seed sample data (optional)
docker compose -f docker-compose.prod.yml exec fastapi \
  python -m backend.fastapi_service.scripts.seed_data
```

### Service Health Checks

```bash
# Check all services
docker compose -f docker-compose.prod.yml ps

# View specific service logs
docker compose -f docker-compose.prod.yml logs fastapi -n 50
docker compose -f docker-compose.prod.yml logs django -n 50
docker compose -f docker-compose.prod.yml logs celery -n 50

# Stream logs in real-time
docker compose -f docker-compose.prod.yml logs -f fastapi
```

### Performance Monitoring

```bash
# Resource usage
docker stats

# Database connections
docker compose -f docker-compose.prod.yml exec postgres \
  psql -U sip_user -d sip_prod -c "SELECT datname, usename, count(*) FROM pg_stat_activity GROUP BY datname, usename;"

# Redis memory usage
docker compose -f docker-compose.prod.yml exec redis \
  redis-cli info memory

# Celery active tasks
docker compose -f docker-compose.prod.yml exec fastapi \
  celery -A backend.fastapi_service.app.tasks.celery_app.celery_app inspect active
```

---

## Production Best Practices

### 1. Security
- ✅ Use strong passwords (min 32 chars, mixed case + symbols)
- ✅ Enable SSL/TLS certificates in Nginx
- ✅ Set `DJANGO_DEBUG=0` in production
- ✅ Use environment-specific secrets management (AWS Secrets Manager, HashiCorp Vault)
- ✅ Regularly update base images: `docker compose pull`
- ✅ Scan images for vulnerabilities: `docker scan myimage`

### 2. Performance
- ✅ FastAPI: 4 workers default (adjust based on CPU cores)
- ✅ Django: 4 workers default (tune for your workload)
- ✅ Redis: LRU eviction with 512MB max memory
- ✅ PostgreSQL: Connection pooling via SQLAlchemy
- ✅ Celery: Concurrency=4, 1000 tasks per child process
- ✅ Frontend: Built static files served by Nginx

### 3. Reliability
- ✅ All services have health checks (30s interval)
- ✅ Restart policy: `unless-stopped` (survives reboots)
- ✅ Named volumes for data persistence
- ✅ Structured logging with rotation (10MB per file, 5 files kept)
- ✅ Database backups: `postgres_backups` volume

### 4. Scalability
- ✅ Use Docker Swarm or Kubernetes for multi-node deployments
- ✅ External load balancer (AWS ALB, Nginx)
- ✅ Managed PostgreSQL (AWS RDS, Azure Database)
- ✅ Managed Redis (AWS ElastiCache, Azure Cache)
- ✅ CDN for frontend assets (CloudFront, Cloudflare)

---

## Backup & Recovery

### PostgreSQL Backups

```bash
# Full backup
docker compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U sip_user sip_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
docker compose -f docker-compose.prod.yml exec postgres \
  psql -U sip_user sip_prod < backup_20240510_120000.sql

# Automated daily backups (in docker-compose.prod.yml)
docker-compose creates: postgres_backups volume
```

### Redis Persistence

```bash
# Redis RDB snapshot
docker compose -f docker-compose.prod.yml exec redis \
  redis-cli BGSAVE

# Check persistence
docker compose -f docker-compose.prod.yml exec redis \
  redis-cli LASTSAVE
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check container logs
docker logs sip_fastapi
docker logs sip_django
docker logs sip_postgres

# Validate configuration
docker compose -f docker-compose.prod.yml config

# Try rebuilding
docker compose -f docker-compose.prod.yml build --no-cache fastapi
```

### Database Connection Issues

```bash
# Verify PostgreSQL is accessible
docker compose -f docker-compose.prod.yml exec postgres \
  pg_isready -U sip_user -d sip_prod

# Check connection from FastAPI
docker compose -f docker-compose.prod.yml exec fastapi \
  python -c "from backend.fastapi_service.app.db.session import SessionLocal; db = SessionLocal(); print('Connected!')"
```

### Redis Connection Issues

```bash
# Test Redis connectivity
docker compose -f docker-compose.prod.yml exec redis \
  redis-cli ping

# Check with password
docker compose -f docker-compose.prod.yml exec redis \
  redis-cli -a $REDIS_PASSWORD ping
```

### High Memory Usage

```bash
# Monitor services
docker stats

# Celery: reduce concurrency or tasks per child
# Redis: implement TTL on keys, adjust maxmemory-policy
# PostgreSQL: tune shared_buffers and work_mem
```

---

## Updates & Maintenance

### Rolling Updates

```bash
# Pull latest images
docker compose -f docker-compose.prod.yml pull

# Rebuild affected services
docker compose -f docker-compose.prod.yml build --no-cache fastapi

# Restart service (with downtime)
docker compose -f docker-compose.prod.yml up -d fastapi

# Verify
docker compose -f docker-compose.prod.yml ps
```

### Database Migrations

```bash
# Backup first
docker compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U sip_user sip_prod > pre_migration_backup.sql

# Run migrations
docker compose -f docker-compose.prod.yml exec django \
  python manage.py migrate

# Verify schema
docker compose -f docker-compose.prod.yml exec postgres \
  psql -U sip_user -d sip_prod -c "\dt"
```

---

## Production Checklist

- [ ] SSL certificates configured in Nginx
- [ ] Strong passwords (32+ chars) for all services
- [ ] DJANGO_DEBUG=0 and DEBUG=False
- [ ] Backup strategy in place (daily PostgreSQL dumps)
- [ ] Monitoring & alerting configured (Prometheus, DataDog)
- [ ] Log aggregation set up (ELK, Splunk)
- [ ] CDN configured for frontend static assets
- [ ] Rate limiting enabled on API endpoints
- [ ] Database indexes optimized
- [ ] Celery workers scaled appropriately
- [ ] Redis eviction policy configured
- [ ] Load balancer health checks enabled
- [ ] Auto-scaling policies defined
- [ ] Incident response plan documented
- [ ] Security scanning (image scanning, OWASP) enabled

---

## Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/concepts/)
- [Django Production Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [Redis Best Practices](https://redis.io/topics/client-side-caching)
- [Nginx Production Configuration](https://nginx.org/en/docs/http/configuring_https_servers.html)

---

**Last Updated:** 2024-05-10
**Version:** 1.0.0
