from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.controllers.comment_controller import (
    create_comment_controller,
    delete_comment_controller,
    get_comment_controller,
    list_comments_controller,
    update_comment_controller,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentQueryParams, CommentResponse, CommentUpdate
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[CommentResponse])
def list_comments(
    note_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None, max_length=120),
    sort_by: str = Query("created_at", pattern="^(created_at|updated_at)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    author_id: UUID | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    params = CommentQueryParams(
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        author_id=author_id,
    )
    return list_comments_controller(db, current_user, note_id, params)


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    note_id: UUID,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_comment_controller(db, current_user, note_id, payload)


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(
    note_id: UUID,
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_comment_controller(db, current_user, note_id, comment_id)


@router.patch("/{comment_id}", response_model=CommentResponse)
def update_comment(
    note_id: UUID,
    comment_id: UUID,
    payload: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_comment_controller(db, current_user, note_id, comment_id, payload)


@router.delete("/{comment_id}", response_model=dict)
def delete_comment(
    note_id: UUID,
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_comment_controller(db, current_user, note_id, comment_id)
