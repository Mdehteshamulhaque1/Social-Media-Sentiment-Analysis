from __future__ import annotations

import httpx


class FastAPIOrchestrator:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip('/')

    async def fetch_health(self) -> dict[str, object]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f'{self.base_url}/health')
            response.raise_for_status()
            return response.json()

    async def fetch_metrics(self) -> dict[str, object]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f'{self.base_url}/metrics/overview')
            response.raise_for_status()
            return response.json()
