# Docker Security & Performance Best Practices

## Security Best Practices

### 1. Image Security
```bash
# Scan images for vulnerabilities
docker scan sentiment-intelligence-fastapi

# Use minimal base images
FROM python:3.11-slim  # Better than python:3.11 (900MB smaller)

# Keep base images updated
docker pull python:3.11-slim
docker compose build --no-cache
```

### 2. Runtime Security
```dockerfile
# Don't run as root
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Use read-only filesystem where possible
RUN chmod -R 755 /app

# Remove unnecessary packages
RUN apt-get remove --purge -y \
    apt \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

### 3. Secrets Management
```bash
# DON'T commit .env to git
echo ".env.production" >> .gitignore

# Use Docker secrets (Swarm mode)
docker secret create db_password - < db_password.txt

# Or use external secret management
# - AWS Secrets Manager
# - HashiCorp Vault
# - Azure Key Vault
```

### 4. Network Security
```yaml
# Use named networks
networks:
  sip_network:
    driver: bridge

# Don't expose unnecessary ports
ports:
  - '5432:5432'  # Only if needed from outside

# Use environment variables for credentials
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}  # Not hardcoded
```

---

## Performance Optimization

### 1. Image Layer Optimization
```dockerfile
# Order layers from least to most frequently changed
FROM python:3.11-slim

# 1. Install system dependencies (rarely changes)
RUN apt-get update && apt-get install -y curl

# 2. Install Python packages (sometimes changes)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 3. Copy application code (frequently changes)
COPY . .
```

### 2. Build Optimization
```bash
# Use BuildKit for better caching
export DOCKER_BUILDKIT=1

# Parallel builds
docker buildx build --platform linux/amd64,linux/arm64 .

# Build cache mounts
docker build --build-context=requirements=type=cache .
```

### 3. Runtime Optimization
```yaml
# FastAPI: Tune worker count based on CPU cores
fastapi:
  command: uvicorn app:app 
    --workers 4        # = CPU cores for I/O-bound
    --worker-class uvicorn.workers.UvicornWorker

# Django: Tune for workload
django:
  command: gunicorn app:app
    --workers 4        # = (2 × CPU cores) + 1 for I/O
    --worker-class sync
    --worker-tmp-dir /dev/shm  # Faster than disk

# Celery: Scale workers independently
celery:
  deploy:
    replicas: 3
    resources:
      limits:
        cpus: '1'
        memory: 512M
```

### 4. Memory Optimization
```yaml
# Redis: Implement eviction policy
redis:
  command: redis-server
    --maxmemory 512mb
    --maxmemory-policy allkeys-lru  # Evict oldest keys

# Database: Connection pooling
environment:
  DATABASE_POOL_SIZE: 20
  DATABASE_MAX_OVERFLOW: 40
```

### 5. Logging Optimization
```yaml
# Structured logging in JSON
logging:
  driver: json-file
  options:
    max-size: "10m"      # Rotate at 10MB
    max-file: "5"        # Keep 5 rotated logs
    labels: "com.example.service=fastapi"
```

---

## Database Performance

### 1. PostgreSQL Tuning
```yaml
postgres:
  environment:
    POSTGRES_INIT_ARGS: >
      --shared_buffers=256MB
      --effective_cache_size=1GB
      --maintenance_work_mem=64MB
      --work_mem=16MB
      --wal_buffers=16MB
```

### 2. Connection Pooling
```python
# SQLAlchemy pool configuration
from sqlalchemy import create_engine

engine = create_engine(
    database_url,
    pool_size=20,           # Open connections
    max_overflow=40,        # Temporary overflow
    pool_pre_ping=True,     # Verify connections before use
    pool_recycle=3600,      # Recycle after 1 hour
)
```

### 3. Query Optimization
```sql
-- Add indexes for frequent queries
CREATE INDEX idx_sentiment_analysis_user_id 
  ON sentiment_analysis(user_id);

-- Analyze execution plans
EXPLAIN ANALYZE SELECT * FROM sentiment_analysis 
  WHERE user_id = 123;
```

---

## Monitoring & Debugging

### 1. Health Checks
```yaml
healthcheck:
  test: ['CMD', 'curl', '-f', 'http://localhost:8000/health']
  interval: 30s       # Check every 30 seconds
  timeout: 10s        # Wait 10 seconds for response
  retries: 3          # Mark unhealthy after 3 failures
  start_period: 40s   # Grace period on startup
```

### 2. Resource Limits
```yaml
services:
  fastapi:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '1'
          memory: 512M
```

### 3. Metrics Collection
```bash
# Enable Prometheus metrics
docker compose exec fastapi curl http://localhost:8000/metrics

# Monitor with DataDog
docker compose exec -e DD_AGENT_HOST=datadog-agent \
  fastapi python -m pip install datadog
```

### 4. Logging Aggregation
```yaml
# Forward logs to ELK Stack
logging:
  driver: awslogs
  options:
    awslogs-group: /ecs/sip
    awslogs-region: us-east-1
    awslogs-stream-prefix: ecs
```

---

## Troubleshooting

### 1. Out of Memory
```bash
# Check memory usage
docker stats

# Increase container memory
docker compose up -d --scale fastapi=1
# Or modify docker-compose.yml:
#   deploy:
#     resources:
#       limits:
#         memory: 2G

# Analyze memory leaks
docker top sip_fastapi
ps aux | grep python
```

### 2. High CPU Usage
```bash
# Identify bottlenecks
docker exec sip_fastapi top -b -n 1

# Profile with py-spy
docker exec -it sip_fastapi py-spy record -o profile.svg -- python -m uvicorn

# Reduce worker concurrency
# Modify docker-compose.yml: --workers 2
```

### 3. Slow Queries
```bash
# Enable PostgreSQL query logging
docker compose exec postgres psql -U sip_user -d sip_prod \
  -c "ALTER SYSTEM SET log_min_duration_statement = 1000;"

# Restart PostgreSQL to apply changes
docker compose restart postgres

# Check logs
docker compose logs postgres | grep duration
```

---

## Production Checklist

- [ ] **Security**: Run `docker scan` on all images
- [ ] **Security**: All services run as non-root user
- [ ] **Security**: Secrets stored in `.env` (not committed to git)
- [ ] **Performance**: Worker counts optimized for CPU cores
- [ ] **Performance**: Database connection pooling configured
- [ ] **Performance**: Indexes created for common queries
- [ ] **Performance**: Build layers optimized with BuildKit
- [ ] **Monitoring**: Health checks configured for all services
- [ ] **Monitoring**: Structured logging with JSON format
- [ ] **Monitoring**: Alerts set up for unhealthy services
- [ ] **Reliability**: Database backups automated
- [ ] **Reliability**: Restart policies set to `unless-stopped`
- [ ] **Scalability**: Services can scale horizontally
- [ ] **Scalability**: Reverse proxy (Nginx) configured
- [ ] **Compliance**: SSL/TLS certificates installed
- [ ] **Compliance**: CORS properly configured
- [ ] **Documentation**: Deployment procedures documented

---

## Resources

- [Docker Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Compose Best Practices](https://docs.docker.com/compose/compose-file/compose-file-v3/#services)
- [PostgreSQL Performance](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/latest/configure.html)
