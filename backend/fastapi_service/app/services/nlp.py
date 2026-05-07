from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Any

POSITIVE_HINTS = {"great", "love", "excellent", "awesome", "happy", "strong", "improved"}
NEGATIVE_HINTS = {"bad", "hate", "awful", "terrible", "sad", "weak", "broken"}
TOXIC_HINTS = {"idiot", "stupid", "useless", "trash"}


@dataclass
class NLPResult:
    text: str
    sentiment: str
    confidence: float
    emotion: str
    toxicity: float
    sarcasm_hint: float
    keywords: list[str]
    hashtags: list[str]
    language: str

    def asdict(self) -> dict[str, Any]:
        return self.__dict__


class NLPService:
    def __init__(self) -> None:
        self.transformer = self._load_transformer()

    def _load_transformer(self):
        try:
            from transformers import pipeline  # type: ignore

            return pipeline("sentiment-analysis")
        except Exception:
            return None

    def analyze(self, text: str, language: str | None = None) -> dict[str, Any]:
        cleaned = self._preprocess(text)
        if self.transformer is not None:
            prediction = self.transformer(text[:512])[0]
            label = str(prediction["label"]).lower()
            score = float(prediction["score"])
            sentiment = self._normalize_label(label)
            confidence = round(score, 3)
        else:
            sentiment, confidence = self._lexical_sentiment(cleaned)

        emotion = self._detect_emotion(cleaned, sentiment)
        toxicity = self._toxicity_score(cleaned)
        sarcasm_hint = self._sarcasm_score(cleaned)
        keywords = self._keywords(cleaned)
        hashtags = re.findall(r"#\w+", text)

        result = NLPResult(
            text=text,
            sentiment=sentiment,
            confidence=confidence,
            emotion=emotion,
            toxicity=toxicity,
            sarcasm_hint=sarcasm_hint,
            keywords=keywords,
            hashtags=hashtags,
            language=language or self._detect_language(text),
        )
        return result.asdict()

    def _preprocess(self, text: str) -> list[str]:
        tokens = re.findall(r"[a-zA-Z#']+", text.lower())
        return [token for token in tokens if token not in {"the", "and", "for", "with", "this", "that"}]

    def _normalize_label(self, label: str) -> str:
        if "pos" in label or label == "label_2":
            return "positive"
        if "neg" in label or label == "label_0":
            return "negative"
        return "neutral"

    def _lexical_sentiment(self, tokens: list[str]) -> tuple[str, float]:
        pos = sum(token in POSITIVE_HINTS for token in tokens)
        neg = sum(token in NEGATIVE_HINTS for token in tokens)
        total = max(pos + neg, 1)
        score = (pos - neg) / total
        if score > 0.05:
            return "positive", round(0.55 + min(score, 1.0) * 0.4, 3)
        if score < -0.05:
            return "negative", round(0.55 + min(abs(score), 1.0) * 0.4, 3)
        return "neutral", 0.58

    def _detect_emotion(self, tokens: list[str], sentiment: str) -> str:
        token_set = set(tokens)
        if token_set & {"angry", "frustrated", "annoyed"}:
            return "anger"
        if token_set & {"excited", "thrilled", "amazing"}:
            return "joy"
        if token_set & {"worried", "concerned", "risk"}:
            return "fear"
        return {"positive": "joy", "negative": "sadness"}.get(sentiment, "neutral")

    def _toxicity_score(self, tokens: list[str]) -> float:
        toxic_hits = sum(token in TOXIC_HINTS for token in tokens)
        return round(min(toxic_hits / max(len(tokens), 1) * 4, 1.0), 3)

    def _sarcasm_score(self, tokens: list[str]) -> float:
        has_positive_and_negative = bool(set(tokens) & POSITIVE_HINTS and set(tokens) & NEGATIVE_HINTS)
        irony_markers = any(token in {"yeah", "sure", "totally", "obviously"} for token in tokens)
        score = 0.62 if has_positive_and_negative or irony_markers else 0.18
        return round(score, 3)

    def _keywords(self, tokens: list[str]) -> list[str]:
        filtered = [token for token in tokens if len(token) > 3 and not token.startswith("#")]
        return [word for word, _ in Counter(filtered).most_common(6)]

    def _detect_language(self, text: str) -> str:
        if any(char in text for char in "éàèùçñ"):
            return "fr"
        if any(char in text for char in "¿¡"):
            return "es"
        return "en"
