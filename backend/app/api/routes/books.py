from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.controllers.book_controller import (
    create_book_controller,
    delete_book_controller,
    get_book_controller,
    list_books_controller,
    update_book_controller,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.book import BookCreate, BookQueryParams, BookResponse, BookUpdate
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[BookResponse])
def list_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None, max_length=120),
    sort_by: str = Query("created_at", pattern="^(title|created_at|updated_at)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    created_from: datetime | None = None,
    created_to: datetime | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    params = BookQueryParams(
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        created_from=created_from,
        created_to=created_to,
    )
    return list_books_controller(db, current_user, params)


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_book_controller(db, current_user, payload)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_book_controller(db, current_user, book_id)


@router.patch("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: UUID,
    payload: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_book_controller(db, current_user, book_id, payload)


@router.delete("/{book_id}", response_model=dict)
def delete_book(book_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_book_controller(db, current_user, book_id)
