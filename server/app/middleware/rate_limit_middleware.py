from collections import defaultdict, deque
import time

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.storage: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request, call_next):
        client = request.client.host if request.client else "anonymous"
        is_auth_route = request.url.path.startswith(f"{settings.api_v1_prefix}/auth")
        limit = settings.auth_rate_limit_max_requests if is_auth_route else settings.rate_limit_max_requests
        window = settings.rate_limit_window_seconds
        key = f"{client}:{'auth' if is_auth_route else 'general'}"

        now = time.time()
        bucket = self.storage[key]
        while bucket and now - bucket[0] > window:
            bucket.popleft()

        if len(bucket) >= limit:
            return JSONResponse(
                status_code=429,
                content={"success": False, "message": "Too many requests, please try again later"},
            )

        bucket.append(now)
        return await call_next(request)
