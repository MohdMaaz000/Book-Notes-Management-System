from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.comment import CommentCreate, CommentQueryParams, CommentResponse, CommentUpdate
from app.services.comment_service import comment_service


def list_comments_controller(db: Session, user: User, note_id: UUID, params: CommentQueryParams) -> dict:
    result = comment_service.list_comments(db, user, note_id, params)
    return {"items": [CommentResponse.model_validate(item) for item in result["items"]], "meta": result["meta"]}


def create_comment_controller(db: Session, user: User, note_id: UUID, payload: CommentCreate) -> CommentResponse:
    return CommentResponse.model_validate(comment_service.create_comment(db, user, note_id, payload))


def get_comment_controller(db: Session, user: User, note_id: UUID, comment_id: UUID) -> CommentResponse:
    return CommentResponse.model_validate(comment_service.get_comment(db, user, note_id, comment_id))


def update_comment_controller(
    db: Session, user: User, note_id: UUID, comment_id: UUID, payload: CommentUpdate
) -> CommentResponse:
    return CommentResponse.model_validate(comment_service.update_comment(db, user, note_id, comment_id, payload))


def delete_comment_controller(db: Session, user: User, note_id: UUID, comment_id: UUID) -> dict:
    comment_service.delete_comment(db, user, note_id, comment_id)
    return {"message": "Comment deleted successfully"}
