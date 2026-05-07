# Sentiment Intelligence Platform

Production-oriented monorepo for social media sentiment intelligence, built around a FastAPI analytics engine, Django admin/auth orchestration, Redis/Celery background processing, PostgreSQL persistence, and a modern React dashboard.

## Architecture

- `backend/fastapi_service`: async analytics API, WebSockets, caching, and task orchestration.
- `backend/django_admin`: auth, RBAC, team/workspace management, and operational administration.
- `frontend`: React dashboard with Tailwind, Framer Motion, and chart-driven analytics views.
- `shared`: cross-service contracts, enums, and utility functions.
- `infra`: Docker and Nginx deployment assets.

## Core capabilities

- Real-time sentiment, emotion, toxicity, and keyword extraction.
- Historical analytics, trend comparison, CSV uploads, and report generation.
- Team workspaces, audit logs, API usage metrics, notifications, and saved reports.
- Redis caching, Celery jobs, WebSocket updates, and structured logging.

## Local run flow

1. Copy `.env.example` to `.env` and fill the service credentials.
2. Start the stack with Docker Compose.
3. Open the React dashboard, API docs, and admin service through the reverse proxy.

### Seed realistic analytics data

Run this from the repository root after dependencies are installed:

`python -m backend.fastapi_service.scripts.seed_data`

This writes sample sentiment events into PostgreSQL (or fallback memory if DB is unavailable) so the dashboard can render non-empty analytics views immediately.

## Service map

- FastAPI analytics: `backend/fastapi_service/app/main.py`
- Django orchestration: `backend/django_admin/config/settings.py`
- Frontend shell: `frontend/src/App.tsx`
- Deployment: `docker-compose.yml`

## Design intent

The UI is intentionally styled as an enterprise analytics product, with dark/light mode, glass panels, live charts, and operational status surfaces rather than a basic CRUD admin.