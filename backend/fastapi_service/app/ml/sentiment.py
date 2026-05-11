from typing import Tuple
from transformers import pipeline
from ..core.config import settings


class SentimentModel:
    def __init__(self, model_name: str = None):
        model_name = model_name or settings.HF_MODEL_NAME
        self._pipe = pipeline("sentiment-analysis", model=model_name)

    def predict(self, text: str) -> Tuple[str, float]:
        res = self._pipe(text, truncation=True)
        if not res:
            return "neutral", 0.0
        r = res[0]
        label = r.get("label")
        score = float(r.get("score", 0.0))
        return label.lower(), score


# singleton
model = SentimentModel()
