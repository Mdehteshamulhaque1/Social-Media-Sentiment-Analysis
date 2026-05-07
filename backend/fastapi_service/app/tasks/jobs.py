from __future__ import annotations

from collections import Counter
from typing import Any

from backend.fastapi_service.app.tasks.celery_app import celery_app
from shared.text import top_terms


@celery_app.task(name="refresh_workspace_summary")
def refresh_workspace_summary(workspace_id: str, analyses: list[dict[str, Any]]) -> dict[str, Any]:
    sentiments = Counter(item["sentiment"] for item in analyses)
    return {
        "workspace_id": workspace_id,
        "total": len(analyses),
        "sentiment_breakdown": dict(sentiments),
        "top_keywords": top_terms([item.get("text", "") for item in analyses]),
    }


@celery_app.task(name="build_report_artifact")
def build_report_artifact(report_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "report_id": report_id,
        "artifact": f"/tmp/reports/{report_id}.pdf",
        "status": "generated",
        "metadata": payload,
    }


@celery_app.task(name="process_csv_upload")
def process_csv_upload(upload_id: str, row_count: int) -> dict[str, Any]:
    return {
        "upload_id": upload_id,
        "processed_rows": row_count,
        "status": "completed",
    }
