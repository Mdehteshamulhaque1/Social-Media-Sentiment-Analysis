from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):
    analysis_id: str
    workspace_id: str | None = None
    text: str
    sentiment: str
    confidence: float
    emotion: str
    toxicity: float
    sarcasm_hint: float
    keywords: list[str] = Field(default_factory=list)
    hashtags: list[str] = Field(default_factory=list)
    language: str = "en"
    summary: str | None = None
    created_at: datetime


class WorkspaceOverview(BaseModel):
    workspace_id: str
    name: str
    member_count: int
    total_analyses: int
    positive_share: float
    negative_share: float
    health_score: float
