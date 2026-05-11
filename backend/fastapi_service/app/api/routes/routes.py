from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, WebSocket, WebSocketDisconnect
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies.deps import get_current_user
from ...database.session import get_db
from ...schemas.schemas import PredictionIn, PredictionOut, BatchPredictIn, Token, UserCreate
from ...services.predict_service import predict_and_store, batch_predict_texts, get_history
from ...services.auth_service import create_user, authenticate_user, create_token_for_user
from ...realtime.ws_manager import manager
from ...utils.redis_cache import cache

import hashlib, json
from ...models.models import Prediction
from sqlalchemy import select

router = APIRouter()


@router.get("/api/v1/health", tags=["health"])
async def health():
    return {"status": "ok"}


@router.get("/api/v1/metrics", tags=["metrics"])
async def metrics(db: AsyncSession = Depends(get_db)):
    total = await db.execute("SELECT count(*) FROM predictions")
    cnt = total.scalar() or 0
    return {"predictions_count": cnt}


@router.post("/api/v1/auth/register", response_model=Token, tags=["auth"])
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, user_in)
    token = create_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/api/v1/auth/token", response_model=Token, tags=["auth"])
async def login(form_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/api/v1/predict", response_model=PredictionOut, tags=["predict"])
async def predict(payload: PredictionIn, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    key = hashlib.sha256(payload.text.encode("utf-8")).hexdigest()
    cached = await cache.get(f"pred:{key}")
    if cached:
        data = json.loads(cached.decode())
        # still persist the usage
        pred = await predict_and_store(db, payload.text, user_id=current_user.id)
        return {"id": pred.id, "text": pred.text, "label": data["label"], "score": data["score"], "user_id": pred.user_id, "created_at": pred.created_at}
    pred = await predict_and_store(db, payload.text, user_id=current_user.id)
    # cache the model result
    await cache.set(f"pred:{key}", json.dumps({"label": pred.label, "score": pred.score}).encode(), expire=60 * 60)
    return pred


@router.post("/api/v1/batch-predict", response_model=List[PredictionOut], tags=["predict"])
async def batch_predict(payload: BatchPredictIn, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    results = await batch_predict_texts(db, payload.texts, user_id=current_user.id)
    return results


@router.get("/api/v1/history", response_model=List[PredictionOut], tags=["predict"])
async def history(
    page: int = 1,
    size: int = 20,
    label: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # build query with filters and pagination
    q = select(Prediction).order_by(Prediction.created_at.desc())
    if label:
        q = q.where(Prediction.label == label)
    if start_date:
        q = q.where(Prediction.created_at >= start_date)
    if end_date:
        q = q.where(Prediction.created_at <= end_date)
    q = q.offset((page - 1) * size).limit(size)
    res = await db.execute(q)
    return res.scalars().all()


@router.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"ack: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
