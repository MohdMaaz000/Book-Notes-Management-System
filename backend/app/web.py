from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import logger
from app.core.paths import STATIC_DIR, TEMPLATES_DIR
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.book import BookCreate, BookQueryParams
from app.schemas.note import NoteCreate, NoteQueryParams, NoteUpdate
from app.services.auth_service import auth_service
from app.services.book_service import book_service
from app.services.note_service import note_service
from app.utils.exceptions import AppError

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
web_router = APIRouter(include_in_schema=False)


def _template_context(request: Request, **context):
    base_context = {
        "request": request,
        "current_user": request.session.get("user"),
        "app_name": "Book & Notes Management System",
        "flash_messages": request.session.pop("flash_messages", []),
    }
    base_context.update(context)
    return base_context


def _validation_error_message(exc: ValidationError) -> str:
    first_error = exc.errors()[0]
    field = str(first_error["loc"][-1]).replace("_", " ").capitalize()
    return f"{field}: {first_error['msg']}"


def _set_refresh_cookie(response: RedirectResponse, token: str) -> None:
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_exp_days)
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=token,
        httponly=True,
        secure=settings.is_production,
        samesite="strict",
        expires=expires_at,
    )


def _clear_refresh_cookie(response: RedirectResponse) -> None:
    response.delete_cookie(key=settings.refresh_cookie_name)


def _store_user_session(request: Request, user: User) -> None:
    request.session["user"] = {"id": str(user.id), "name": user.name, "email": user.email}


def _push_flash_message(request: Request, message: str, category: str = "success") -> None:
    flash_messages = request.session.setdefault("flash_messages", [])
    flash_messages.append({"message": message, "category": category})
    request.session["flash_messages"] = flash_messages


def _get_session_user(request: Request, db: Session) -> User:
    user_data = request.session.get("user")
    if not user_data or not user_data.get("id"):
        raise AppError(401, "Please log in to continue")

    user = db.get(User, UUID(user_data["id"]))
    if not user:
        request.session.clear()
        raise AppError(401, "Please log in to continue")
    return user


def _redirect(path: str) -> RedirectResponse:
    return RedirectResponse(url=path, status_code=303)


@web_router.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse(STATIC_DIR / "favicon.svg", media_type="image/svg+xml")


@web_router.get("/robots.txt")
def robots() -> FileResponse:
    return FileResponse(STATIC_DIR / "robots.txt", media_type="text/plain; charset=utf-8")


@web_router.get("/")
def landing_page(request: Request):
    if request.session.get("user"):
        return _redirect("/books")
    return templates.TemplateResponse(request, "index.html", _template_context(request, page_title="Book & Notes Management System"))


@web_router.get("/register")
def register_page(request: Request):
    if request.session.get("user"):
        return _redirect("/books")
    return templates.TemplateResponse(
        request,
        "auth.html",
        _template_context(
            request,
            page_title="Register",
            form_title="Build your study space",
            subtitle="Create your account and manage books and notes from one organized place.",
            submit_label="Create account",
            alternate_label="Already have an account?",
            alternate_href="/login",
            alternate_link_text="Login",
            form_action="/register",
            mode="register",
        ),
    )


@web_router.post("/register")
def register_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        payload = RegisterRequest(name=name, email=email, password=password)
        user, _, refresh_token = auth_service.register(db, payload.name, payload.email, payload.password)
    except ValidationError as exc:
        logger.info("Register form validation failed for email=%s: %s", email, exc.errors())
        return templates.TemplateResponse(
            request,
            "auth.html",
            _template_context(
                request,
                page_title="Register",
                form_title="Build your study space",
                subtitle="Create your account and manage books and notes from one organized place.",
                submit_label="Create account",
                alternate_label="Already have an account?",
                alternate_href="/login",
                alternate_link_text="Login",
                form_action="/register",
                mode="register",
                error=_validation_error_message(exc),
                form_data={"name": name, "email": email},
            ),
            status_code=400,
        )
    except AppError as exc:
        logger.info("Register request rejected for email=%s: %s", email, exc.message)
        return templates.TemplateResponse(
            request,
            "auth.html",
            _template_context(
                request,
                page_title="Register",
                form_title="Build your study space",
                subtitle="Create your account and manage books and notes from one organized place.",
                submit_label="Create account",
                alternate_label="Already have an account?",
                alternate_href="/login",
                alternate_link_text="Login",
                form_action="/register",
                mode="register",
                error=exc.message,
                form_data={"name": name, "email": email},
            ),
            status_code=400,
        )
    except Exception:  # noqa: BLE001
        logger.exception("Register form failed unexpectedly for email=%s", email)
        return templates.TemplateResponse(
            request,
            "auth.html",
            _template_context(
                request,
                page_title="Register",
                form_title="Build your study space",
                subtitle="Create your account and manage books and notes from one organized place.",
                submit_label="Create account",
                alternate_label="Already have an account?",
                alternate_href="/login",
                alternate_link_text="Login",
                form_action="/register",
                mode="register",
                error="Unable to create your account right now",
                form_data={"name": name, "email": email},
            ),
            status_code=500,
        )

    _store_user_session(request, user)
    _push_flash_message(request, "Account created successfully.")
    response = _redirect("/books")
    _set_refresh_cookie(response, refresh_token)
    return response


@web_router.get("/login")
def login_page(request: Request):
    if request.session.get("user"):
        return _redirect("/books")
    return templates.TemplateResponse(
        request,
        "auth.html",
        _template_context(
            request,
            page_title="Login",
            form_title="Sign in to your workspace",
            subtitle="Continue managing books, topics, and notes from your Python-backed workspace.",
            submit_label="Login",
            alternate_label="New here?",
            alternate_href="/register",
            alternate_link_text="Register",
            form_action="/login",
            mode="login",
        ),
    )


@web_router.post("/login")
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        payload = LoginRequest(email=email, password=password)
        user, _, refresh_token = auth_service.login(db, payload.email, payload.password)
    except ValidationError as exc:
        logger.info("Login form validation failed for email=%s: %s", email, exc.errors())
        return templates.TemplateResponse(
            request,
            "auth.html",
            _template_context(
                request,
                page_title="Login",
                form_title="Sign in to your workspace",
                subtitle="Continue managing books, topics, and notes from your Python-backed workspace.",
                submit_label="Login",
                alternate_label="New here?",
                alternate_href="/register",
                alternate_link_text="Register",
                form_action="/login",
                mode="login",
                error=_validation_error_message(exc),
                form_data={"email": email},
            ),
            status_code=400,
        )
    except AppError as exc:
        logger.info("Login request rejected for email=%s: %s", email, exc.message)
        return templates.TemplateResponse(
            request,
            "auth.html",
            _template_context(
                request,
                page_title="Login",
                form_title="Sign in to your workspace",
                subtitle="Continue managing books, topics, and notes from your Python-backed workspace.",
                submit_label="Login",
                alternate_label="New here?",
                alternate_href="/register",
                alternate_link_text="Register",
                form_action="/login",
                mode="login",
                error=exc.message,
                form_data={"email": email},
            ),
            status_code=400,
        )
    except Exception:  # noqa: BLE001
        logger.exception("Login form failed unexpectedly for email=%s", email)
        return templates.TemplateResponse(
            request,
            "auth.html",
            _template_context(
                request,
                page_title="Login",
                form_title="Sign in to your workspace",
                subtitle="Continue managing books, topics, and notes from your Python-backed workspace.",
                submit_label="Login",
                alternate_label="New here?",
                alternate_href="/register",
                alternate_link_text="Register",
                form_action="/login",
                mode="login",
                error="Unable to log you in right now",
                form_data={"email": email},
            ),
            status_code=500,
        )

    _store_user_session(request, user)
    _push_flash_message(request, "Welcome back.")
    response = _redirect("/books")
    _set_refresh_cookie(response, refresh_token)
    return response


@web_router.post("/logout")
def logout_submit(request: Request):
    request.session.clear()
    _push_flash_message(request, "You have been logged out.")
    response = _redirect("/")
    _clear_refresh_cookie(response)
    return response


@web_router.get("/books")
def books_page(request: Request, db: Session = Depends(get_db), search: str | None = None):
    try:
        user = _get_session_user(request, db)
        result = book_service.list_books(
            db,
            user,
            BookQueryParams(page=1, page_size=100, search=search, sort_by="updated_at", sort_order="desc"),
        )
    except AppError:
        return _redirect("/login")

    return templates.TemplateResponse(request, "books.html", _template_context(request, books=result["items"], search=search or "", page_title="Books"))


@web_router.post("/books")
def create_book_submit(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        user = _get_session_user(request, db)
        book_service.create_book(db, user, BookCreate(title=title, description=description or None))
        _push_flash_message(request, "Book created successfully.")
        return _redirect("/books")
    except ValidationError as exc:
        logger.info("Book form validation failed for user_id=%s: %s", request.session.get("user", {}).get("id"), exc.errors())
        user = _get_session_user(request, db)
        result = book_service.list_books(
            db,
            user,
            BookQueryParams(page=1, page_size=100, sort_by="updated_at", sort_order="desc"),
        )
        return templates.TemplateResponse(
            request,
            "books.html",
            _template_context(
                request,
                books=result["items"],
                search="",
                page_title="Books",
                error=_validation_error_message(exc),
                form_data={"title": title, "description": description},
            ),
            status_code=400,
        )
    except AppError as exc:
        result = book_service.list_books(
            db,
            user,
            BookQueryParams(page=1, page_size=100, sort_by="updated_at", sort_order="desc"),
        )
        return templates.TemplateResponse(
            request,
            "books.html",
            _template_context(
                request,
                books=result["items"],
                search="",
                page_title="Books",
                error=exc.message,
                form_data={"title": title, "description": description},
            ),
            status_code=400,
        )
    except Exception:  # noqa: BLE001
        logger.exception("Book form failed unexpectedly for user_id=%s", request.session.get("user", {}).get("id"))
        user = _get_session_user(request, db)
        result = book_service.list_books(
            db,
            user,
            BookQueryParams(page=1, page_size=100, sort_by="updated_at", sort_order="desc"),
        )
        return templates.TemplateResponse(
            request,
            "books.html",
            _template_context(
                request,
                books=result["items"],
                search="",
                page_title="Books",
                error="Unable to create the book right now",
                form_data={"title": title, "description": description},
            ),
            status_code=500,
        )


@web_router.post("/books/{book_id}/delete")
def delete_book_submit(request: Request, book_id: UUID, db: Session = Depends(get_db)):
    try:
        user = _get_session_user(request, db)
        book_service.delete_book(db, user, book_id)
        _push_flash_message(request, "Book deleted successfully.")
    except AppError:
        pass
    return _redirect("/books")


@web_router.get("/books/{book_id}")
def book_detail_page(request: Request, book_id: UUID, db: Session = Depends(get_db), search: str | None = None):
    try:
        user = _get_session_user(request, db)
        book = book_service.get_book(db, user, book_id)
        notes = note_service.list_notes(
            db,
            user,
            book_id,
            NoteQueryParams(page=1, page_size=100, search=search, sort_by="updated_at", sort_order="desc"),
        )["items"]
    except AppError:
        return _redirect("/books")

    return templates.TemplateResponse(request, "book_detail.html", _template_context(request, book=book, notes=notes, search=search or "", page_title=book.title))


@web_router.post("/books/{book_id}/notes")
def create_note_submit(
    request: Request,
    book_id: UUID,
    title: str = Form(...),
    content: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        user = _get_session_user(request, db)
        note_service.create_note(db, user, book_id, NoteCreate(title=title, content=content))
        _push_flash_message(request, "Note added successfully.")
        return _redirect(f"/books/{book_id}")
    except ValidationError as exc:
        logger.info("Note form validation failed for book_id=%s: %s", book_id, exc.errors())
        user = _get_session_user(request, db)
        book = book_service.get_book(db, user, book_id)
        notes = note_service.list_notes(
            db,
            user,
            book_id,
            NoteQueryParams(page=1, page_size=100, sort_by="updated_at", sort_order="desc"),
        )["items"]
        return templates.TemplateResponse(
            request,
            "book_detail.html",
            _template_context(
                request,
                book=book,
                notes=notes,
                search="",
                page_title=book.title,
                error=_validation_error_message(exc),
                note_form_data={"title": title, "content": content},
            ),
            status_code=400,
        )
    except AppError as exc:
        book = book_service.get_book(db, user, book_id)
        notes = note_service.list_notes(
            db,
            user,
            book_id,
            NoteQueryParams(page=1, page_size=100, sort_by="updated_at", sort_order="desc"),
        )["items"]
        return templates.TemplateResponse(
            request,
            "book_detail.html",
            _template_context(
                request,
                book=book,
                notes=notes,
                search="",
                page_title=book.title,
                error=exc.message,
                note_form_data={"title": title, "content": content},
            ),
            status_code=400,
        )
    except Exception:  # noqa: BLE001
        logger.exception("Note form failed unexpectedly for book_id=%s", book_id)
        user = _get_session_user(request, db)
        book = book_service.get_book(db, user, book_id)
        notes = note_service.list_notes(
            db,
            user,
            book_id,
            NoteQueryParams(page=1, page_size=100, sort_by="updated_at", sort_order="desc"),
        )["items"]
        return templates.TemplateResponse(
            request,
            "book_detail.html",
            _template_context(
                request,
                book=book,
                notes=notes,
                search="",
                page_title=book.title,
                error="Unable to create the note right now",
                note_form_data={"title": title, "content": content},
            ),
            status_code=500,
        )


@web_router.post("/books/{book_id}/notes/{note_id}")
def update_note_submit(
    request: Request,
    book_id: UUID,
    note_id: UUID,
    title: str = Form(...),
    content: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        user = _get_session_user(request, db)
        note_service.update_note(db, user, book_id, note_id, NoteUpdate(title=title, content=content))
        _push_flash_message(request, "Note saved successfully.")
    except AppError:
        pass
    return _redirect(f"/books/{book_id}")


@web_router.post("/books/{book_id}/notes/{note_id}/delete")
def delete_note_submit(request: Request, book_id: UUID, note_id: UUID, db: Session = Depends(get_db)):
    try:
        user = _get_session_user(request, db)
        note_service.delete_note(db, user, book_id, note_id)
        _push_flash_message(request, "Note deleted successfully.")
    except AppError:
        pass
    return _redirect(f"/books/{book_id}")
