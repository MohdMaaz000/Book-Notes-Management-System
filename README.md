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
- Railway + Neon deployment support

## Project Structure

```text
backend/
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
cd backend
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
cd backend
alembic upgrade head
```

Create a new migration after model changes:

```bash
cd backend
alembic revision --autogenerate -m "describe change"
```

## Testing

```bash
cd backend
pytest
```

## Docker

```bash
docker compose up --build
```

## Railway + Neon Deployment

This project works well with:

- Neon for managed PostgreSQL
- Railway for hosting the FastAPI app

Recommended setup:

1. Create a PostgreSQL database in Neon.
2. Copy the Neon connection string into `DATABASE_URL`.
3. Deploy the `backend/` service on Railway.
4. Set the app environment variables in Railway.
5. Run `alembic upgrade head` before the app goes live.
6. Open the deployed URL and verify the health check, frontend, and auth flow.

Suggested Railway service settings:

- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`
- Pre-deploy command: `alembic upgrade head`
- Health check path: `/api/v1/health`

Required environment variables:

- `DATABASE_URL`
- `JWT_ACCESS_SECRET`
- `JWT_REFRESH_SECRET`
- `SESSION_SECRET`

Recommended environment variables:

- `APP_NAME=Book & Notes Management System`
- `ENVIRONMENT=production`
- `API_V1_PREFIX=/api/v1`
- `HOST=0.0.0.0`
- `JWT_ACCESS_EXP_MINUTES=15`
- `JWT_REFRESH_EXP_DAYS=7`
- `JWT_ALGORITHM=HS256`
- `REFRESH_COOKIE_NAME=book_notes_refresh_token`
- `BCRYPT_ROUNDS=12`
- `RATE_LIMIT_WINDOW_SECONDS=900`
- `RATE_LIMIT_MAX_REQUESTS=200`
- `AUTH_RATE_LIMIT_MAX_REQUESTS=20`

For browser access after deployment, update:

- `CORS_ORIGINS` with your Railway app URL

Example:

```env
CORS_ORIGINS=["https://your-app-name.up.railway.app"]
```

Neon note:

- Use the Neon PostgreSQL connection string directly as `DATABASE_URL`.
- If Neon provides multiple URLs, prefer the pooled connection string for app traffic and keep SSL enabled in the URL.

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
