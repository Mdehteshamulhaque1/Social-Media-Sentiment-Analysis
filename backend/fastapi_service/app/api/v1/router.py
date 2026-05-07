from fastapi import APIRouter

from backend.fastapi_service.app.api.v1.endpoints.analysis import router as analysis_router
from backend.fastapi_service.app.api.v1.endpoints.health import router as health_router
from backend.fastapi_service.app.api.v1.endpoints.metrics import router as metrics_router
from backend.fastapi_service.app.api.v1.endpoints.reports import router as reports_router
from backend.fastapi_service.app.api.v1.endpoints.workspaces import router as workspaces_router


api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(metrics_router, prefix="/metrics", tags=["metrics"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
api_router.include_router(workspaces_router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(reports_router, prefix="/reports", tags=["reports"])
