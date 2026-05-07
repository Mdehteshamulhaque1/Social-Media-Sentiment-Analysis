from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any

from backend.fastapi_service.app.services.nlp import NLPService


nlp_service = NLPService()


def analyze_text_batch(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [nlp_service.analyze(item["text"], language=item.get("language")) for item in items]


def summarize_insights(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "summary": f"{result['sentiment'].title()} sentiment with {result['confidence']:.2f} confidence.",
        "top_keywords": result.get("keywords", [])[:4],
        "trend": "upward" if result["sentiment"] == "positive" else "mixed",
    }


def build_overview(dataset: list[dict[str, Any]]) -> dict[str, Any]:
    sentiments = Counter(item["sentiment"] for item in dataset)
    confidences = [item.get("confidence", 0.0) for item in dataset]
    return {
        "total": len(dataset),
        "sentiments": sentiments,
        "avg_confidence": round(mean(confidences), 3) if confidences else 0.0,
        "top_keywords": [word for word, _ in Counter(word for item in dataset for word in item.get("keywords", [])).most_common(8)],
    }
