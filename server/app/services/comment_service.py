from uuid import UUID

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.comment import Comment
from app.models.note import Note
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentQueryParams, CommentUpdate
from app.utils.exceptions import AppError
from app.utils.pagination import build_pagination_meta


class CommentService:
    sort_map = {"created_at": Comment.created_at, "updated_at": Comment.updated_at}

    def _get_owned_note(self, db: Session, user: User, note_id: UUID) -> Note:
        note = db.scalar(
            select(Note).join(Book, Note.book_id == Book.id).where(Note.id == note_id, Book.user_id == user.id)
        )
        if not note:
            raise AppError(404, "Note not found")
        return note

    def list_comments(self, db: Session, user: User, note_id: UUID, params: CommentQueryParams) -> dict:
        self._get_owned_note(db, user, note_id)
        query = select(Comment).where(Comment.note_id == note_id)
        if params.search:
            query = query.where(Comment.content.ilike(f"%{params.search}%"))
        if params.author_id:
            query = query.where(Comment.user_id == params.author_id)

        total_items = db.scalar(select(func.count()).select_from(query.subquery())) or 0
        order_column = self.sort_map[params.sort_by]
        order_clause = asc(order_column) if params.sort_order == "asc" else desc(order_column)
        items = db.scalars(
            query.order_by(order_clause).offset((params.page - 1) * params.page_size).limit(params.page_size)
        ).all()

        return {"items": items, "meta": build_pagination_meta(params.page, params.page_size, total_items)}

    def create_comment(self, db: Session, user: User, note_id: UUID, payload: CommentCreate) -> Comment:
        self._get_owned_note(db, user, note_id)
        comment = Comment(note_id=note_id, user_id=user.id, content=payload.content)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    def get_comment(self, db: Session, user: User, note_id: UUID, comment_id: UUID) -> Comment:
        self._get_owned_note(db, user, note_id)
        comment = db.scalar(select(Comment).where(Comment.id == comment_id, Comment.note_id == note_id))
        if not comment:
            raise AppError(404, "Comment not found")
        return comment

    def update_comment(self, db: Session, user: User, note_id: UUID, comment_id: UUID, payload: CommentUpdate) -> Comment:
        comment = self.get_comment(db, user, note_id, comment_id)
        if comment.user_id != user.id:
            raise AppError(403, "You can only update your own comments")
        comment.content = payload.content
        db.commit()
        db.refresh(comment)
        return comment

    def delete_comment(self, db: Session, user: User, note_id: UUID, comment_id: UUID) -> None:
        comment = self.get_comment(db, user, note_id, comment_id)
        if comment.user_id != user.id:
            raise AppError(403, "You can only delete your own comments")
        db.delete(comment)
        db.commit()


comment_service = CommentService()
