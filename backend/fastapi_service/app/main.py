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
