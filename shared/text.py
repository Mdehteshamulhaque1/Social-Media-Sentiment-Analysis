from __future__ import annotations

import re
from collections import Counter


def normalize_text(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z#']+", text.lower())
    return [token for token in tokens if len(token) > 2]


def top_terms(texts: list[str], limit: int = 8) -> list[str]:
    counter = Counter(token for text in texts for token in normalize_text(text))
    return [word for word, _ in counter.most_common(limit)]
