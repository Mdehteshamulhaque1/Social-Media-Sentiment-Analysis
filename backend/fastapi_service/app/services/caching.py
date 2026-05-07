from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

try:
    import redis
except Exception:  # pragma: no cover - optional in scaffold
    redis = None


@dataclass
class CacheClient:
    backend: Any = None
    fallback: dict[str, tuple[Any, int | None]] = field(default_factory=dict)

    def get(self, key: str) -> Any:
        if self.backend is not None:
            value = self.backend.get(key)
            return json.loads(value) if value else None
        entry = self.fallback.get(key)
        return entry[0] if entry else None

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        if self.backend is not None:
            self.backend.setex(key, ttl, json.dumps(value))
            return
        self.fallback[key] = (value, ttl)


cache = CacheClient()
