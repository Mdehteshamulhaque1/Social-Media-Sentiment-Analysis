from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class PredictionIn(BaseModel):
    text: str


class PredictionOut(BaseModel):
    id: int
    text: str
    label: str
    score: float
    user_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


class BatchPredictIn(BaseModel):
    texts: List[str]
