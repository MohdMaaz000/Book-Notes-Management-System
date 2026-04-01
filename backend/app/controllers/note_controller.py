from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.note import NoteCreate, NoteQueryParams, NoteResponse, NoteUpdate
from app.services.note_service import note_service


def list_notes_controller(db: Session, user: User, book_id: UUID, params: NoteQueryParams) -> dict:
    result = note_service.list_notes(db, user, book_id, params)
    return {"items": [NoteResponse.model_validate(item) for item in result["items"]], "meta": result["meta"]}


def create_note_controller(db: Session, user: User, book_id: UUID, payload: NoteCreate) -> NoteResponse:
    return NoteResponse.model_validate(note_service.create_note(db, user, book_id, payload))


def get_note_controller(db: Session, user: User, book_id: UUID, note_id: UUID) -> NoteResponse:
    return NoteResponse.model_validate(note_service.get_note(db, user, book_id, note_id))


def update_note_controller(db: Session, user: User, book_id: UUID, note_id: UUID, payload: NoteUpdate) -> NoteResponse:
    return NoteResponse.model_validate(note_service.update_note(db, user, book_id, note_id, payload))


def delete_note_controller(db: Session, user: User, book_id: UUID, note_id: UUID) -> dict:
    note_service.delete_note(db, user, book_id, note_id)
    return {"message": "Note deleted successfully"}
