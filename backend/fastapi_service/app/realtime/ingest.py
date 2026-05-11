from .ws_manager import manager
from ..ml.sentiment import model as hf_model
from ..database.session import AsyncSessionLocal
from ..models.models import Prediction
import asyncio


async def process_streamed_text(text: str, user_id: int = None):
    # predict
    label, score = hf_model.predict(text)
    # persist using a fresh session
    async with AsyncSessionLocal() as db:
        pred = Prediction(text=text, label=label, score=score, user_id=user_id)
        db.add(pred)
        await db.commit()
        await db.refresh(pred)
    # broadcast to websocket clients
    await manager.broadcast({"text": text, "label": label, "score": score})
