# Production Deployment Verification Checklist

Use this checklist before deploying to production to ensure all components are properly configured.

---

## 📋 Pre-Deployment Checklist

### Environment & Configuration

- [ ] `.env.production` file created and properly secured
- [ ] All `change_me` placeholders have been replaced
- [ ] `POSTGRES_PASSWORD` is strong (32+ chars, mixed case, symbols)
- [ ] `DJANGO_SECRET_KEY` generated and unique
- [ ] `REDIS_PASSWORD` is strong (32+ chars, mixed case, symbols)
- [ ] `DJANGO_DEBUG=0` (production mode enabled)
- [ ] `APP_ENV=production` set
- [ ] `ALLOWED_HOSTS` includes your production domain(s)
- [ ] `CORS_ORIGINS` configured for your frontend domain(s)
- [ ] `.env.production` added to `.gitignore`
- [ ] No `.env` files committed to repository
- [ ] Database credentials are not hardcoded anywhere

### Docker Images

- [ ] All Dockerfiles use `.prod` versions from generator
- [ ] Base images are minimal (alpine/slim)
- [ ] All services run as non-root user
- [ ] No unnecessary packages installed
- [ ] Health checks configured for all services
- [ ] Image scanning completed: `docker scan <image>`
- [ ] Images pushed to private registry (optional but recommended)

### Docker Compose Configuration

- [ ] `docker-compose.prod.yml` being used (not development version)
- [ ] Service restart policies set to `unless-stopped`
- [ ] Named network configured for service isolation
- [ ] Persistent volumes created for databases
- [ ] Log rotation configured (max-size, max-file)
- [ ] Health check intervals and timeouts appropriate
- [ ] Service dependencies properly configured
- [ ] Port mappings reviewed and necessary

### Security

- [ ] SSL/TLS certificates installed in `infra/nginx/ssl/`
- [ ] Nginx SSL configuration updated
- [ ] SECURE_SSL_REDIRECT=True in Django settings
- [ ] SESSION_COOKIE_SECURE=True
- [ ] CSRF_COOKIE_SECURE=True
- [ ] HSTS headers configured (SECURE_HSTS_SECONDS=31536000)
- [ ] PostgreSQL password protected (not default)
- [ ] Redis password protected with authentication
- [ ] Database backups enabled and tested
- [ ] Secret storage reviewed (AWS Secrets Manager, Vault, etc.)
- [ ] API rate limiting configured
- [ ] CORS properly restricted (not `*`)

### Database

- [ ] PostgreSQL 16 Alpine image selected
- [ ] Database name matches configuration
- [ ] Database user created with limited privileges
- [ ] Backup volume configured (`postgres_backups`)
- [ ] Connection pooling parameters configured
- [ ] Database migrations run successfully
- [ ] Indexes created for common queries
- [ ] Query logging enabled for performance monitoring
- [ ] Backup strategy documented and automated

### Cache & Message Queue

- [ ] Redis 7 Alpine image selected
- [ ] Redis password authentication enabled
- [ ] Redis persistence (AOF/RDB) configured
- [ ] Redis memory limits set (maxmemory, maxmemory-policy)
- [ ] Celery broker URL configured
- [ ] Celery result backend configured
- [ ] Celery worker concurrency tuned for CPU cores
- [ ] Task timeouts configured

### FastAPI Service

- [ ] Uvicorn workers set to appropriate count (4 by default)
- [ ] Worker class set (uvloop recommended)
- [ ] Health check endpoint accessible
- [ ] API documentation disabled in production (optional)
- [ ] Structured logging configured
- [ ] Error handling properly implemented
- [ ] CORS middleware configured
- [ ] Timeout settings appropriate for workload

### Django Service

- [ ] Gunicorn workers set appropriately (4 by default)
- [ ] Gunicorn worker class configured
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] Media files directory configured
- [ ] Database migrations applied
- [ ] Superuser account created
- [ ] Admin interface security review done
- [ ] Email backend configured (if needed)
- [ ] Celery integration tested

### Frontend

- [ ] React build optimized for production
- [ ] Environment variables correctly set
- [ ] VITE_API_BASE_URL points to production API
- [ ] Asset caching headers configured in Nginx
- [ ] SPA routing configured in Nginx
- [ ] Static files served with gzip compression
- [ ] Source maps excluded from production build

### Nginx Reverse Proxy

- [ ] SSL certificates properly configured
- [ ] SSL/TLS version restricted (1.2+)
- [ ] Cipher suites hardened
- [ ] HSTS header added
- [ ] X-Frame-Options set to DENY/SAMEORIGIN
- [ ] X-Content-Type-Options set to nosniff
- [ ] Content-Security-Policy header configured
- [ ] Gzip compression enabled
- [ ] Caching headers configured
- [ ] Rate limiting configured
- [ ] Request/response logging enabled

### Monitoring & Logging

- [ ] Log aggregation service configured (ELK, Splunk, etc.)
- [ ] Alert thresholds defined
- [ ] Healthcheck monitoring enabled
- [ ] Resource usage monitoring active
- [ ] Error rate monitoring configured
- [ ] Performance metrics collection enabled
- [ ] Database query logging enabled
- [ ] Structured logging format validated
- [ ] Log retention policy defined

### Backup & Disaster Recovery

- [ ] PostgreSQL backup automated (daily, tested)
- [ ] Redis persistence verified
- [ ] Backup storage location identified
- [ ] Backup retention policy documented
- [ ] Disaster recovery plan documented
- [ ] Backup restoration tested (dry-run)
- [ ] Point-in-time recovery capability verified
- [ ] Backup encryption enabled

### Performance

- [ ] Database connection pooling configured
- [ ] Redis maxmemory eviction policy set
- [ ] Database indexes optimized
- [ ] Query performance verified (< 100ms)
- [ ] FastAPI workers count optimized for CPU
- [ ] Django workers count optimized
- [ ] Celery concurrency tuned
- [ ] Static asset caching configured
- [ ] Database statistics up to date
- [ ] Slow query logging enabled

### Scaling & Load Balancing

- [ ] Load balancer configured (if multi-node)
- [ ] Health check endpoints verified
- [ ] Service discovery configured (if applicable)
- [ ] Auto-scaling policies defined (if cloud-based)
- [ ] Horizontal scaling tested
- [ ] Session affinity reviewed (if needed)
- [ ] Distributed tracing configured (optional)

### Testing

- [ ] Load testing completed (k6, locust)
- [ ] Failover testing performed
- [ ] Database failover tested
- [ ] API endpoint testing completed
- [ ] SSL/TLS verification done
- [ ] Security scanning completed (OWASP ZAP, Burp)
- [ ] Performance profiling completed
- [ ] Disaster recovery drill executed

### Documentation

- [ ] Deployment procedure documented
- [ ] Runbook created for common issues
- [ ] Password/credentials documented securely
- [ ] Architecture diagram updated
- [ ] Configuration documented
- [ ] Team onboarding documentation prepared
- [ ] Incident response procedure defined
- [ ] On-call rotation established

### Final Sign-Off

- [ ] All checklist items completed
- [ ] Security review approved
- [ ] Performance review approved
- [ ] Architecture review approved
- [ ] Team lead sign-off obtained
- [ ] Production deployment authorized

---

## 🔍 Pre-Deployment Verification Script

```bash
#!/bin/bash

echo "Running pre-deployment verification..."

# Check Docker
docker --version || { echo "✗ Docker not found"; exit 1; }
echo "✓ Docker installed"

# Check docker-compose
docker compose version || { echo "✗ Docker Compose not found"; exit 1; }
echo "✓ Docker Compose installed"

# Check .env file
[ -f .env.production ] || { echo "✗ .env.production not found"; exit 1; }
echo "✓ .env.production exists"

# Check for secrets in .env
if grep -q "change_me" .env.production; then
    echo "✗ ERROR: Placeholder values found in .env.production"
    exit 1
fi
echo "✓ No placeholder values in .env.production"

# Check Dockerfile.prod files
[ -f backend/fastapi_service/Dockerfile.prod ] || { echo "✗ FastAPI Dockerfile.prod missing"; exit 1; }
[ -f backend/django_admin/Dockerfile.prod ] || { echo "✗ Django Dockerfile.prod missing"; exit 1; }
[ -f frontend/Dockerfile.prod ] || { echo "✗ Frontend Dockerfile.prod missing"; exit 1; }
echo "✓ All production Dockerfiles exist"

# Check docker-compose.prod.yml
[ -f docker-compose.prod.yml ] || { echo "✗ docker-compose.prod.yml not found"; exit 1; }
echo "✓ docker-compose.prod.yml exists"

# Validate docker-compose config
docker compose -f docker-compose.prod.yml config > /dev/null || { echo "✗ docker-compose.prod.yml validation failed"; exit 1; }
echo "✓ docker-compose.prod.yml is valid"

# Check SSL certificates if needed
# if grep -q "ssl" docker-compose.prod.yml; then
#     [ -d "infra/nginx/ssl" ] && [ -f "infra/nginx/ssl/cert.pem" ] || { echo "✗ SSL certificates not found"; exit 1; }
#     echo "✓ SSL certificates found"
# fi

echo ""
echo "✅ All pre-deployment checks passed!"
echo ""
echo "Next steps:"
echo "  1. Review docker-compose.prod.yml resource limits"
echo "  2. Configure SSL certificates in infra/nginx/ssl/"
echo "  3. Run: docker compose -f docker-compose.prod.yml up -d"
echo "  4. Monitor: docker compose -f docker-compose.prod.yml logs -f"
```

---

## ⚠️ Common Pre-Deployment Issues

### Issue: Docker Compose Version
**Problem:** Old docker-compose command instead of docker compose
**Solution:** Update Docker Desktop to v20.10+

### Issue: Permission Denied on Scripts
**Problem:** `./deploy.sh` returns permission denied
**Solution:** `chmod +x deploy.sh`

### Issue: Port Already in Use
**Problem:** Port 80, 443, or database port already in use
**Solution:** Change ports in `docker-compose.prod.yml` or stop conflicting service

### Issue: Out of Disk Space
**Problem:** Docker build fails due to no space
**Solution:** `docker system prune -a` (after backing up data)

### Issue: Image Build Failure
**Problem:** `pip install` fails in Dockerfile
**Solution:** Check internet connection, update base image, increase timeout

### Issue: Database Connection Failed
**Problem:** FastAPI can't connect to PostgreSQL
**Solution:** Ensure PostgreSQL is healthy, check credentials, wait 60s for initialization

### Issue: SSL Certificate Error
**Problem:** HTTPS requests fail
**Solution:** Verify certificate paths, check Nginx configuration

---

## 📞 Rollback Procedure

If deployment fails, follow this rollback procedure:

```bash
# 1. Stop current deployment
docker compose -f docker-compose.prod.yml down

# 2. Restore previous database backup
docker run --rm -v postgres_data:/data -v $(pwd)/backups:/backups \
  postgres:16-alpine \
  psql -U sip_user -d sip_prod < /backups/backup_YYYYMMDD_HHMMSS.sql

# 3. Start with previous image version
docker compose -f docker-compose.prod.yml up -d --build=false

# 4. Verify services
docker compose -f docker-compose.prod.yml ps

# 5. Check logs
docker compose -f docker-compose.prod.yml logs
```

---

**Last Updated:** May 10, 2024  
**Version:** 1.0.0
