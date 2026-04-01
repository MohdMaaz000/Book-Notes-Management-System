from uuid import UUID

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate, BookQueryParams, BookUpdate
from app.utils.exceptions import AppError
from app.utils.pagination import build_pagination_meta


class BookService:
    sort_map = {
        "title": Book.title,
        "created_at": Book.created_at,
        "updated_at": Book.updated_at,
    }

    def list_books(self, db: Session, user: User, params: BookQueryParams) -> dict:
        query = select(Book).where(Book.user_id == user.id)
        if params.search:
            query = query.where(Book.title.ilike(f"%{params.search}%"))
        if params.created_from:
            query = query.where(Book.created_at >= params.created_from)
        if params.created_to:
            query = query.where(Book.created_at <= params.created_to)

        total_items = db.scalar(select(func.count()).select_from(query.subquery())) or 0
        order_column = self.sort_map[params.sort_by]
        order_clause = asc(order_column) if params.sort_order == "asc" else desc(order_column)

        items = db.scalars(
            query.order_by(order_clause).offset((params.page - 1) * params.page_size).limit(params.page_size)
        ).all()

        return {"items": items, "meta": build_pagination_meta(params.page, params.page_size, total_items)}

    def create_book(self, db: Session, user: User, payload: BookCreate) -> Book:
        book = Book(user_id=user.id, title=payload.title, description=payload.description)
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    def get_book(self, db: Session, user: User, book_id: UUID) -> Book:
        book = db.scalar(select(Book).where(Book.id == book_id, Book.user_id == user.id))
        if not book:
            raise AppError(404, "Book not found")
        return book

    def update_book(self, db: Session, user: User, book_id: UUID, payload: BookUpdate) -> Book:
        book = self.get_book(db, user, book_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(book, field, value)
        db.commit()
        db.refresh(book)
        return book

    def delete_book(self, db: Session, user: User, book_id: UUID) -> None:
        book = self.get_book(db, user, book_id)
        db.delete(book)
        db.commit()


book_service = BookService()
