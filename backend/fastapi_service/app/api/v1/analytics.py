from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Optional, List
from datetime import datetime, timedelta

from ...database.session import get_db
from ...models.models import Prediction
from ...schemas.schemas import PredictionOut
from ...api.deps import get_current_user

router = APIRouter(prefix="/api/v1/analytics")


@router.get("/trends", response_model=List[dict], tags=["analytics"])
async def sentiment_trends(
    days: int = Query(7, gt=0, le=365),
    label: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # aggregate daily counts for last `days`
    since = datetime.utcnow() - timedelta(days=days)
    sql = """
    SELECT date_trunc('day', created_at) AS day, label, count(*) AS cnt
    FROM predictions
    WHERE created_at >= :since
    """
    if label:
        sql += " AND label = :label"
    sql += " GROUP BY day, label ORDER BY day"

    res = await db.execute(text(sql), {"since": since, "label": label} if label else {"since": since})
    rows = res.fetchall()
    out = []
    for row in rows:
        out.append({"day": row[0].isoformat(), "label": row[1], "count": int(row[2])})
    return out


@router.get("/top_keywords", tags=["analytics"])
async def top_keywords(limit: int = 20, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    # simple keyword extraction from recent predictions
    sql = "SELECT text FROM predictions ORDER BY created_at DESC LIMIT 1000"
    res = await db.execute(text(sql))
    rows = res.fetchall()
    from collections import Counter
    import re

    counter = Counter()
    for (txt,) in rows:
        words = re.findall(r"#?\w{3,}", txt.lower())
        counter.update(words)
    common = counter.most_common(limit)
    return [{"term": k, "count": v} for k, v in common]
