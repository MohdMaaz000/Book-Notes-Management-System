from uuid import UUID

from fastapi import Cookie, Depends, Header
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.utils.exceptions import AppError


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise AppError(401, "Access token is required")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
    except Exception as exc:  # noqa: BLE001
        raise AppError(401, "Invalid or expired access token") from exc

    user = db.get(User, UUID(payload["sub"]))
    if not user:
        raise AppError(401, "User not found")
    return user


def get_refresh_token_cookie(
    refresh_token: str | None = Cookie(default=None, alias=settings.refresh_cookie_name),
) -> str:
    if not refresh_token:
        raise AppError(401, "Refresh token is required")
    return refresh_token
