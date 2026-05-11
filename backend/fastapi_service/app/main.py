import logging
import asyncio

from fastapi import FastAPI, Response, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from prometheus_client import Counter, Histogram
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import routes as api_routes
from .database import close_db, init_db
from .core.config import settings
from .utils.redis_cache import cache
from .realtime.streamer import get_default_streamer
from .realtime.ingest import process_streamed_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUESTS = Counter("sentiment_requests_total", "Total sentiment requests")
PREDICTION_LATENCY = Histogram("sentiment_prediction_seconds", "Prediction latency seconds")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    # rate limiter
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_routes.router)

    @app.get("/metrics")
    async def metrics():
        data = generate_latest()
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)

    @app.on_event("startup")
    async def on_startup():
        logger.info("Initializing database connection")
        await init_db()
        # connect cache
        try:
            await cache.connect()
        except Exception:
            logger.warning("Could not connect to Redis cache on startup")

        # start dummy streamer for realtime demo
        try:
            streamer = get_default_streamer(callback=process_streamed_text)
            streamer.start()
            logger.info("Started default dummy streamer for realtime data")
        except Exception:
            logger.warning("Failed to start streamer")

    @app.on_event("shutdown")
    async def on_shutdown():
        await close_db()

    return app


app = create_app()
import os

from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import structlog

from backend.fastapi_service.app.api.v1.router import api_router
from backend.fastapi_service.app.core.config import settings
from backend.fastapi_service.app.core.logging import configure_logging
from backend.fastapi_service.app.core.middleware import RequestContextMiddleware
from backend.fastapi_service.app.realtime.manager import realtime_manager

logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="Sentiment Intelligence Platform API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_origin_regex=settings.cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestContextMiddleware)
    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup() -> None:
        logger.info(
            "fastapi_service_startup",
            environment=settings.environment,
            database_configured=bool(settings.resolved_database_url),
            cors_origins=settings.cors_origins,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled_exception", path=request.url.path, method=request.method)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    @app.get("/")
    async def root() -> dict[str, str]:
        return {
            "service": "sentiment-intelligence-platform",
            "status": "operational",
            "environment": settings.environment,
        }

    if os.getenv("VERCEL", "0").lower() not in {"1", "true", "yes"}:
        @app.websocket("/ws/updates")
        async def updates(websocket: WebSocket) -> None:
            await realtime_manager.accept(websocket)
            try:
                while True:
                    await realtime_manager.ping(websocket)
            finally:
                await realtime_manager.disconnect(websocket)

    return app


app = create_app()
