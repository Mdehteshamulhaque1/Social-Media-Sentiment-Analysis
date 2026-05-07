from fastapi import APIRouter

from backend.fastapi_service.app.core.config import settings


router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"service": settings.app_name, "status": "healthy", "environment": settings.environment}
