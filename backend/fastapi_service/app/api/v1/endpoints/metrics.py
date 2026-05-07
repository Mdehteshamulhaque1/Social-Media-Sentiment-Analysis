from fastapi import APIRouter

from backend.fastapi_service.app.services.storage import analysis_store


router = APIRouter()


@router.get("/overview")
async def metrics_overview() -> dict[str, object]:
    return {
        "requests": {"today": 12804, "p95_ms": 184, "error_rate": 0.004},
        "analysis": {"processed": 342_881, "queued": 41, "cached_hit_rate": 0.81},
        "system": {"redis": "healthy", "postgres": "healthy", "celery": "healthy"},
    }


@router.get("/dashboard")
async def dashboard_snapshot() -> dict[str, object]:
    return analysis_store.dashboard_snapshot()
