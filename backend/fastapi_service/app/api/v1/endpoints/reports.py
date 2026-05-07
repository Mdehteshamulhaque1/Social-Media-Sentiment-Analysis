from __future__ import annotations

from fastapi import APIRouter


router = APIRouter()


@router.get("")
async def list_reports() -> dict[str, object]:
    return {
        "items": [
            {"id": "rpt_1", "title": "Weekly Brand Health", "format": "pdf", "status": "ready"},
            {"id": "rpt_2", "title": "Campaign Sentiment", "format": "csv", "status": "processing"},
        ]
    }


@router.post("/generate")
async def generate_report() -> dict[str, object]:
    return {"status": "queued", "report_id": "rpt_generated", "eta_seconds": 45}
