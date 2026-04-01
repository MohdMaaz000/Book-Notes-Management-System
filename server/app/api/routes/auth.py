from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_refresh_token_cookie
from app.controllers.auth_controller import (
    login_controller,
    logout_controller,
    me_controller,
    refresh_controller,
    register_controller,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, MessageResponse, RegisterRequest, UserSummary

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(payload: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    return register_controller(payload, response, db)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    return login_controller(payload, response, db)


@router.post("/refresh", response_model=AuthResponse)
def refresh(response: Response, refresh_token: str = Depends(get_refresh_token_cookie), db: Session = Depends(get_db)):
    return refresh_controller(refresh_token, response, db)


@router.post("/logout", response_model=MessageResponse)
def logout(response: Response, refresh_token: str = Depends(get_refresh_token_cookie), db: Session = Depends(get_db)):
    return logout_controller(refresh_token, response, db)


@router.get("/me", response_model=UserSummary)
def me(current_user: User = Depends(get_current_user)):
    return me_controller(current_user)
