from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from backend.fastapi_service.app.db.base import Base
from backend.fastapi_service.app.db.session import engine
from backend.fastapi_service.app.services.analytics import summarize_insights
from backend.fastapi_service.app.services.nlp import NLPService
from backend.fastapi_service.app.services.storage import analysis_store


SAMPLE_TEXTS = [
    "The new checkout flow is excellent and conversion is improving rapidly.",
    "Support response time was terrible this week and users are frustrated.",
    "Launch campaign is getting strong traction with great engagement.",
    "Pricing update caused confusion, but onboarding quality is still good.",
    "Customers love the new dashboard visuals and reporting speed.",
    "The mobile app feels broken after the latest release.",
]


def run_seed() -> None:
    Base.metadata.create_all(bind=engine)
    nlp = NLPService()

    for text in SAMPLE_TEXTS:
        result = nlp.analyze(text, language="en")
        result["analysis_id"] = str(uuid4())
        result["workspace_id"] = "ws_seeded"
        result["created_at"] = datetime.now(timezone.utc).isoformat()
        result["summary"] = summarize_insights(result)["summary"]
        analysis_store.save_analysis(result)

    print(f"Seeded {len(SAMPLE_TEXTS)} analysis records.")


if __name__ == "__main__":
    run_seed()
