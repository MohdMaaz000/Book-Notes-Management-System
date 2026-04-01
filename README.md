# Book & Notes Management System

Book & Notes Management System is a production-style Python web application for organizing books, topics, and notes in a structured workspace.

It is built to demonstrate strong internship-ready backend and database skills while still working as a complete web product.

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Alembic
- PyJWT
- bcrypt
- Jinja2 templates
- HTML/CSS

## Features

- User registration, login, refresh, and logout flows
- Session-backed frontend plus REST API
- Protected book, note, and comment workflows
- Pagination, search, sorting, and filtering
- Global error handling and request validation
- Request logging and rate limiting
- Environment-based configuration
- Docker deployment support
- Server-rendered frontend with Jinja2 templates
- Render deployment support

## Project Structure

```text
server/
  app/
    api/
    controllers/
    core/
    db/
    middleware/
    models/
    schemas/
    services/
    utils/
    static/
    templates/
  requirements.txt
  Dockerfile
  start.sh
render.yaml
docker-compose.yml
```

## Local Setup

```bash
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

App URLs:

- Frontend: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

## Database Migrations

```bash
cd server
alembic upgrade head
```

Create a new migration after model changes:

```bash
cd server
alembic revision --autogenerate -m "describe change"
```

## Testing

```bash
cd server
pytest
```

## Docker

```bash
docker compose up --build
```

## Render Deployment

The repository includes [`render.yaml`](./render.yaml) for Render deployment.

Deployment model:

- one Render web service
- one managed PostgreSQL database

Recommended start flow:

```bash
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

After deployment, update:

- `CORS_ORIGINS` with your live Render URL
- `JWT_ACCESS_SECRET`
- `JWT_REFRESH_SECRET`
- `SESSION_SECRET`

Example:

```env
CORS_ORIGINS=["https://your-app-name.onrender.com"]
```

## Key API Endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
- `GET|POST /api/v1/books`
- `GET|PATCH|DELETE /api/v1/books/{book_id}`
- `GET|POST /api/v1/books/{book_id}/notes`
- `GET|PATCH|DELETE /api/v1/books/{book_id}/notes/{note_id}`
- `GET|POST /api/v1/notes/{note_id}/comments`
- `GET|PATCH|DELETE /api/v1/notes/{note_id}/comments/{comment_id}`
