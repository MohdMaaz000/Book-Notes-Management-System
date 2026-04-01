from datetime import datetime, timedelta, timezone

from fastapi import Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, MessageResponse, RegisterRequest, UserSummary
from app.services.auth_service import auth_service


def _set_refresh_cookie(response: Response, token: str) -> None:
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_exp_days)
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=token,
        httponly=True,
        secure=settings.is_production,
        samesite="strict",
        expires=expires_at,
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(key=settings.refresh_cookie_name)


def register_controller(payload: RegisterRequest, response: Response, db: Session) -> AuthResponse:
    user, access_token, refresh_token = auth_service.register(db, payload.name, payload.email, payload.password)
    _set_refresh_cookie(response, refresh_token)
    return AuthResponse(user=UserSummary(id=str(user.id), name=user.name, email=user.email), access_token=access_token)


def login_controller(payload: LoginRequest, response: Response, db: Session) -> AuthResponse:
    user, access_token, refresh_token = auth_service.login(db, payload.email, payload.password)
    _set_refresh_cookie(response, refresh_token)
    return AuthResponse(user=UserSummary(id=str(user.id), name=user.name, email=user.email), access_token=access_token)


def refresh_controller(raw_refresh_token: str, response: Response, db: Session) -> AuthResponse:
    user, access_token, refresh_token = auth_service.refresh(db, raw_refresh_token)
    _set_refresh_cookie(response, refresh_token)
    return AuthResponse(user=UserSummary(id=str(user.id), name=user.name, email=user.email), access_token=access_token)


def logout_controller(raw_refresh_token: str | None, response: Response, db: Session) -> MessageResponse:
    auth_service.logout(db, raw_refresh_token)
    _clear_refresh_cookie(response)
    return MessageResponse(message="Logged out successfully")


def me_controller(user: User) -> UserSummary:
    return UserSummary(id=str(user.id), name=user.name, email=user.email)
