from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    hash_token,
    new_token_id,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.utils.exceptions import AppError


class AuthService:
    @staticmethod
    def _normalize_utc(value: datetime) -> datetime:
        # SQLite can return naive datetimes in tests, while PostgreSQL typically returns aware ones.
        return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)

    def register(self, db: Session, name: str, email: str, password: str) -> tuple[User, str, str]:
        existing = db.scalar(select(User).where(User.email == email))
        if existing:
            raise AppError(409, "A user with this email already exists")

        user = User(name=name, email=email, password_hash=hash_password(password))
        db.add(user)
        db.flush()

        access_token, refresh_token = self._issue_tokens(db, user)
        db.commit()
        db.refresh(user)
        return user, access_token, refresh_token

    def login(self, db: Session, email: str, password: str) -> tuple[User, str, str]:
        user = db.scalar(select(User).where(User.email == email))
        if not user or not verify_password(password, user.password_hash):
            raise AppError(401, "Invalid email or password")

        access_token, refresh_token = self._issue_tokens(db, user)
        db.commit()
        return user, access_token, refresh_token

    def refresh(self, db: Session, raw_refresh_token: str) -> tuple[User, str, str]:
        try:
            payload = decode_refresh_token(raw_refresh_token)
        except Exception as exc:  # noqa: BLE001
            raise AppError(401, "Invalid or expired refresh token") from exc

        token_id = UUID(payload["jti"])
        user_id = UUID(payload["sub"])

        token_record = db.get(RefreshToken, token_id)
        if not token_record or token_record.user_id != user_id:
            raise AppError(401, "Refresh token not recognized")
        expires_at = self._normalize_utc(token_record.expires_at)
        if token_record.revoked_at is not None or expires_at <= datetime.now(timezone.utc):
            raise AppError(401, "Refresh token is no longer valid")
        if token_record.token_hash != hash_token(raw_refresh_token):
            raise AppError(401, "Refresh token mismatch")

        user = db.get(User, user_id)
        if not user:
            raise AppError(401, "User not found")

        token_record.revoked_at = datetime.now(timezone.utc)
        access_token, refresh_token = self._issue_tokens(db, user)
        db.commit()
        return user, access_token, refresh_token

    def logout(self, db: Session, raw_refresh_token: str | None) -> None:
        if not raw_refresh_token:
            return

        try:
            payload = decode_refresh_token(raw_refresh_token)
            token_id = UUID(payload["jti"])
        except Exception:  # noqa: BLE001
            return

        token_record = db.get(RefreshToken, token_id)
        if token_record and token_record.revoked_at is None:
            token_record.revoked_at = datetime.now(timezone.utc)
            db.commit()

    def _issue_tokens(self, db: Session, user: User) -> tuple[str, str]:
        access_token = create_access_token(str(user.id), user.email)
        refresh_token_id = new_token_id()
        refresh_token, expires_at = create_refresh_token(str(user.id), refresh_token_id)
        db.add(
            RefreshToken(
                id=UUID(refresh_token_id),
                user_id=user.id,
                token_hash=hash_token(refresh_token),
                expires_at=expires_at,
            )
        )
        return access_token, refresh_token


auth_service = AuthService()
