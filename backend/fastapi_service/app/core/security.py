from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, status

from .config import settings


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return sub
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from enum import Enum
from dataclasses import dataclass

from jose import JWTError, jwt

from backend.fastapi_service.app.core.config import settings


class Role(str, Enum):
    owner = "owner"
    admin = "admin"
    analyst = "analyst"
    viewer = "viewer"


@dataclass(slots=True)
class Principal:
    user_id: str
    email: str
    role: Role
    workspace_id: str | None = None


def create_access_token(subject: str, role: Role, workspace_id: str | None = None) -> str:
    expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
    payload = {
        "sub": subject,
        "role": role.value,
        "workspace_id": workspace_id,
        "exp": expiry,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> Principal:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError("Invalid JWT") from exc

    return Principal(
        user_id=str(payload.get("sub", "")),
        email=str(payload.get("email", "")),
        role=Role(payload.get("role", Role.viewer.value)),
        workspace_id=payload.get("workspace_id"),
    )


def require_roles(*allowed: Role):
    async def dependency(principal: Principal) -> Principal:
        if principal.role not in allowed:
            raise PermissionError("Insufficient role")
        return principal

    return dependency
