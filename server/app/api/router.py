from fastapi import APIRouter

from app.api.routes import auth, books, comments, health, notes
from app.core.config import settings


api_router = APIRouter(prefix=settings.api_v1_prefix)
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(notes.router, prefix="/books/{book_id}/notes", tags=["notes"])
api_router.include_router(comments.router, prefix="/notes/{note_id}/comments", tags=["comments"])
