from __future__ import annotations

from fastapi import APIRouter

from backend.fastapi_service.app.services.insights import generate_insight_summary


router = APIRouter()


@router.get("")
async def list_workspaces() -> dict[str, object]:
    return {
        "items": [
            {"id": "ws_acme", "name": "Acme Growth", "member_count": 8, "health_score": 91.2},
            {"id": "ws_retail", "name": "Retail Intelligence", "member_count": 12, "health_score": 84.6},
        ]
    }


@router.get("/{workspace_id}/overview")
async def workspace_overview(workspace_id: str) -> dict[str, object]:
    dataset = [
        {"sentiment": "positive", "confidence": 0.91},
        {"sentiment": "negative", "confidence": 0.63},
        {"sentiment": "positive", "confidence": 0.82},
    ]
    return {
        "workspace_id": workspace_id,
        "health_score": 88.3,
        "summary": generate_insight_summary(dataset),
        "recent_activity": 24,
    }
