from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from backend.fastapi_service.app.api.v1.router import api_router
from backend.fastapi_service.app.core.config import settings
from backend.fastapi_service.app.core.logging import configure_logging
from backend.fastapi_service.app.core.middleware import RequestContextMiddleware
from backend.fastapi_service.app.db.base import Base
from backend.fastapi_service.app.db.session import engine
from backend.fastapi_service.app.models.analysis import APIUsageEvent, AnalysisRecord
from backend.fastapi_service.app.models.audit import AuditLog
from backend.fastapi_service.app.models.workspace import SavedReport, Workspace
from backend.fastapi_service.app.realtime.manager import realtime_manager


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
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestContextMiddleware)
    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.get("/")
    async def root() -> dict[str, str]:
        return {"service": "sentiment-intelligence-platform", "status": "operational"}

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
