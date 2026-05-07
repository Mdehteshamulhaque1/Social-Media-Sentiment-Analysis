from __future__ import annotations

from fastapi import Depends, Header, HTTPException, status

from backend.fastapi_service.app.core.security import Principal, decode_token
from backend.fastapi_service.app.db.session import get_db


def get_current_principal(authorization: str | None = Header(default=None)) -> Principal:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        return decode_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


def db_dependency():
    return Depends(get_db)
