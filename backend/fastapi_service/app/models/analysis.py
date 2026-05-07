from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.fastapi_service.app.db.base import Base


class AnalysisRecord(Base):
    __tablename__ = "analysis_records"
    __table_args__ = (
        Index("ix_analysis_workspace_created", "workspace_id", "created_at"),
        Index("ix_analysis_sentiment", "sentiment", "confidence"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    workspace_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("workspaces.id"), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(8), default="en")
    sentiment: Mapped[str] = mapped_column(String(16), nullable=False)
    emotion: Mapped[str] = mapped_column(String(32), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    toxicity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    sarcasm_hint: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    keywords: Mapped[dict | list] = mapped_column(JSON, default=list)
    hashtags: Mapped[dict | list] = mapped_column(JSON, default=list)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class APIUsageEvent(Base):
    __tablename__ = "api_usage_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    workspace_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    route: Mapped[str] = mapped_column(String(255), nullable=False)
    method: Mapped[str] = mapped_column(String(12), nullable=False)
    latency_ms: Mapped[int] = mapped_column(default=0)
    status_code: Mapped[int] = mapped_column(default=200)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
