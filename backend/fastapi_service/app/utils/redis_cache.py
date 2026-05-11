import aioredis
from typing import Optional
from ..core.config import settings


class RedisCache:
    def __init__(self, url: str = None):
        self._url = url or settings.REDIS_URL
        self._redis = None

    async def connect(self):
        if self._redis is None:
            self._redis = await aioredis.from_url(self._url)
        return self._redis

    async def get(self, key: str) -> Optional[bytes]:
        r = await self.connect()
        return await r.get(key)

    async def set(self, key: str, value: bytes, expire: int = None):
        r = await self.connect()
        await r.set(key, value, ex=expire)


cache = RedisCache()
