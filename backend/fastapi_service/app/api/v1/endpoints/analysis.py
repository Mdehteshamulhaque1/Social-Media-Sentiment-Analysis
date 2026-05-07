from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from backend.fastapi_service.app.services.analytics import analyze_text_batch, summarize_insights
from backend.fastapi_service.app.services.caching import cache
from backend.fastapi_service.app.services.nlp import NLPService
from backend.fastapi_service.app.services.storage import analysis_store


router = APIRouter()
nlp_service = NLPService()


class TextPayload(BaseModel):
    text: str = Field(min_length=1, max_length=20_000)
    language: str | None = None
    workspace_id: str | None = None


class BatchPayload(BaseModel):
    items: list[TextPayload]


@router.post("/text")
async def analyze_text(payload: TextPayload, background_tasks: BackgroundTasks) -> dict[str, Any]:
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")

    cache_key = f"analysis:{hash(payload.text)}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    result = nlp_service.analyze(payload.text, language=payload.language)
    result["analysis_id"] = str(uuid4())
    result["workspace_id"] = payload.workspace_id
    result["created_at"] = datetime.now(timezone.utc).isoformat()
    result["summary"] = summarize_insights(result)["summary"]

    background_tasks.add_task(cache.set, cache_key, result, ttl=300)
    background_tasks.add_task(analysis_store.save_analysis, result)
    return result


@router.post("/batch")
async def analyze_batch(payload: BatchPayload) -> dict[str, Any]:
    results = analyze_text_batch([item.model_dump() for item in payload.items])
    normalized = []
    for item, result in zip(payload.items, results):
        result["analysis_id"] = str(uuid4())
        result["workspace_id"] = item.workspace_id
        result["created_at"] = datetime.now(timezone.utc).isoformat()
        result["summary"] = summarize_insights(result)["summary"]
        analysis_store.save_analysis(result)
        normalized.append(result)
    return {"items": normalized}


@router.get("/recent")
async def recent_analyses(limit: int = 20) -> dict[str, Any]:
    return {"items": analysis_store.recent_analyses(limit=limit)}


@router.get("/{analysis_id}")
async def get_analysis(analysis_id: UUID) -> dict[str, Any]:
    result = analysis_store.get_analysis(str(analysis_id))
    if result is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result
