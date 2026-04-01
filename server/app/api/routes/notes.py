from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.controllers.note_controller import (
    create_note_controller,
    delete_note_controller,
    get_note_controller,
    list_notes_controller,
    update_note_controller,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.note import NoteCreate, NoteQueryParams, NoteResponse, NoteUpdate
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[NoteResponse])
def list_notes(
    book_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None, max_length=120),
    sort_by: str = Query("updated_at", pattern="^(title|created_at|updated_at)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    updated_from: datetime | None = None,
    updated_to: datetime | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    params = NoteQueryParams(
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        updated_from=updated_from,
        updated_to=updated_to,
    )
    return list_notes_controller(db, current_user, book_id, params)


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    book_id: UUID,
    payload: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_note_controller(db, current_user, book_id, payload)


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    book_id: UUID,
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_note_controller(db, current_user, book_id, note_id)


@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(
    book_id: UUID,
    note_id: UUID,
    payload: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_note_controller(db, current_user, book_id, note_id, payload)


@router.delete("/{note_id}", response_model=dict)
def delete_note(
    book_id: UUID,
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_note_controller(db, current_user, book_id, note_id)
