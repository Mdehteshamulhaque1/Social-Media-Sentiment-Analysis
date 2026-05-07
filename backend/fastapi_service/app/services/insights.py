from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any


def generate_insight_summary(dataset: list[dict[str, Any]]) -> dict[str, Any]:
    if not dataset:
        return {"headline": "No analyses yet", "details": [], "severity": "low"}

    sentiments = Counter(item.get("sentiment", "neutral") for item in dataset)
    avg_confidence = mean(item.get("confidence", 0.0) for item in dataset)
    negative_share = sentiments.get("negative", 0) / len(dataset)
    headline = "Sentiment trend remains stable"
    if negative_share > 0.35:
        headline = "Negative sentiment is accelerating"
    elif sentiments.get("positive", 0) > sentiments.get("negative", 0):
        headline = "Positive momentum is outpacing negative feedback"

    return {
        "headline": headline,
        "avg_confidence": round(avg_confidence, 3),
        "details": [
            f"{sentiments.get('positive', 0)} positive observations",
            f"{sentiments.get('negative', 0)} negative observations",
            f"{sentiments.get('neutral', 0)} neutral observations",
        ],
        "severity": "high" if negative_share > 0.35 else "medium" if negative_share > 0.2 else "low",
    }
