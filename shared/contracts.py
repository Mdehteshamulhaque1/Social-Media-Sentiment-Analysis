from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class SentimentSnapshot:
    id: str
    workspace_id: str | None
    text: str
    sentiment: str
    confidence: float
    emotion: str
    keywords: list[str] = field(default_factory=list)
    hashtags: list[str] = field(default_factory=list)
    created_at: datetime | None = None


@dataclass(slots=True)
class WorkspaceSummary:
    workspace_id: str
    name: str
    member_count: int
    total_analyses: int
    health_score: float
    trend_direction: str


def as_dict(payload: Any) -> dict[str, Any]:
    if hasattr(payload, "__dict__"):
        return dict(payload.__dict__)
    return dict(payload)
