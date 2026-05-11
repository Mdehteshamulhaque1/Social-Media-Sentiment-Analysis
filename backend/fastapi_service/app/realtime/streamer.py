import os
import asyncio
from typing import Callable
from ..core.config import settings

# Note: These streamers are example implementations. Real streaming requires API keys and
# correct setup. These functions demonstrate how to integrate streaming with the app.


class DummyStreamer:
    """A simple dummy streamer that emits sample texts periodically."""
    def __init__(self, callback: Callable[[str], None], interval: float = 5.0):
        self.callback = callback
        self.interval = interval
        self._task = None

    async def _run(self):
        i = 0
        while True:
            text = f"sample message {i} about product and #sale"
            await self.callback(text)
            i += 1
            await asyncio.sleep(self.interval)

    def start(self):
        loop = asyncio.get_event_loop()
        self._task = loop.create_task(self._run())

    def stop(self):
        if self._task:
            self._task.cancel()


async def default_callback(text: str):
    # placeholder callback used when integrating
    print("streamed:", text)


def get_default_streamer(callback: Callable[[str], None] = default_callback):
    return DummyStreamer(callback=callback, interval=3.0)
