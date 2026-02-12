import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class CacheControlMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, cache_control_str: str):
        super().__init__(app)
        self.cache_control_str = cache_control_str

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)
        response.headers["Cache-Control"] = self.cache_control_str
        return response


class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response: Response = await call_next(request)
        process_time = time.perf_counter() - start

        response.headers["X-Process-Time"] = str(process_time)
        return response
