from fastapi import Request, Response
from typing import Callable, Awaitable
import time
from services.metrics_service import MetricsService

metrics_service = MetricsService()

async def metrics_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    metrics_service.record_request_time(request.method, request.url.path, process_time)
    return response
