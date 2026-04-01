from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.book import BookCreate, BookQueryParams, BookResponse, BookUpdate
from app.services.book_service import book_service


def list_books_controller(db: Session, user: User, params: BookQueryParams) -> dict:
    result = book_service.list_books(db, user, params)
    return {"items": [BookResponse.model_validate(item) for item in result["items"]], "meta": result["meta"]}


def create_book_controller(db: Session, user: User, payload: BookCreate) -> BookResponse:
    return BookResponse.model_validate(book_service.create_book(db, user, payload))


def get_book_controller(db: Session, user: User, book_id: UUID) -> BookResponse:
    return BookResponse.model_validate(book_service.get_book(db, user, book_id))


def update_book_controller(db: Session, user: User, book_id: UUID, payload: BookUpdate) -> BookResponse:
    return BookResponse.model_validate(book_service.update_book(db, user, book_id, payload))


def delete_book_controller(db: Session, user: User, book_id: UUID) -> dict:
    book_service.delete_book(db, user, book_id)
    return {"message": "Book deleted successfully"}
