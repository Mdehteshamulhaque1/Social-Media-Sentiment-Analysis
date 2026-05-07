from __future__ import annotations

from celery import Celery

from backend.fastapi_service.app.core.config import settings


celery_app = Celery(
    "sentiment_intelligence",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["backend.fastapi_service.app.tasks.jobs"],
)
celery_app.conf.task_track_started = True
celery_app.conf.result_expires = 3600
