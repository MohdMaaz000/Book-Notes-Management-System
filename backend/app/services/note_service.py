from uuid import UUID

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteQueryParams, NoteUpdate
from app.utils.exceptions import AppError
from app.utils.pagination import build_pagination_meta


class NoteService:
    sort_map = {
        "title": Note.title,
        "created_at": Note.created_at,
        "updated_at": Note.updated_at,
    }

    def _get_owned_book(self, db: Session, user: User, book_id: UUID) -> Book:
        book = db.scalar(select(Book).where(Book.id == book_id, Book.user_id == user.id))
        if not book:
            raise AppError(404, "Book not found")
        return book

    def list_notes(self, db: Session, user: User, book_id: UUID, params: NoteQueryParams) -> dict:
        self._get_owned_book(db, user, book_id)
        query = select(Note).where(Note.book_id == book_id)
        if params.search:
            query = query.where((Note.title.ilike(f"%{params.search}%")) | (Note.content.ilike(f"%{params.search}%")))
        if params.updated_from:
            query = query.where(Note.updated_at >= params.updated_from)
        if params.updated_to:
            query = query.where(Note.updated_at <= params.updated_to)

        total_items = db.scalar(select(func.count()).select_from(query.subquery())) or 0
        order_column = self.sort_map[params.sort_by]
        order_clause = asc(order_column) if params.sort_order == "asc" else desc(order_column)
        items = db.scalars(
            query.order_by(order_clause).offset((params.page - 1) * params.page_size).limit(params.page_size)
        ).all()

        return {"items": items, "meta": build_pagination_meta(params.page, params.page_size, total_items)}

    def create_note(self, db: Session, user: User, book_id: UUID, payload: NoteCreate) -> Note:
        self._get_owned_book(db, user, book_id)
        note = Note(book_id=book_id, title=payload.title, content=payload.content)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    def get_note(self, db: Session, user: User, book_id: UUID, note_id: UUID) -> Note:
        self._get_owned_book(db, user, book_id)
        note = db.scalar(select(Note).where(Note.id == note_id, Note.book_id == book_id))
        if not note:
            raise AppError(404, "Note not found")
        return note

    def update_note(self, db: Session, user: User, book_id: UUID, note_id: UUID, payload: NoteUpdate) -> Note:
        note = self.get_note(db, user, book_id, note_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(note, field, value)
        db.commit()
        db.refresh(note)
        return note

    def delete_note(self, db: Session, user: User, book_id: UUID, note_id: UUID) -> None:
        note = self.get_note(db, user, book_id, note_id)
        db.delete(note)
        db.commit()


note_service = NoteService()
