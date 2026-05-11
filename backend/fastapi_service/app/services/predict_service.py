from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.models import Prediction
from ..ml.sentiment import model as hf_model


async def predict_and_store(db: AsyncSession, text: str, user_id: int = None) -> Prediction:
    label, score = hf_model.predict(text)
    pred = Prediction(text=text, label=label, score=score, user_id=user_id)
    db.add(pred)
    await db.commit()
    await db.refresh(pred)
    return pred


async def batch_predict_texts(db: AsyncSession, texts: list, user_id: int = None):
    results = []
    for t in texts:
        results.append(await predict_and_store(db, t, user_id))
    return results


async def get_history(db: AsyncSession, limit: int = 100):
    q = select(Prediction).order_by(Prediction.created_at.desc()).limit(limit)
    res = await db.execute(q)
    return res.scalars().all()
