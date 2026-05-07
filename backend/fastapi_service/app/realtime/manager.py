from fastapi import WebSocket


class RealtimeManager:
    async def accept(self, websocket: WebSocket) -> None:
        await websocket.accept()

    async def ping(self, websocket: WebSocket) -> None:
        await websocket.send_json({"type": "heartbeat", "status": "ok"})
        await websocket.receive_text()

    async def disconnect(self, websocket: WebSocket) -> None:
        await websocket.close()


realtime_manager = RealtimeManager()
