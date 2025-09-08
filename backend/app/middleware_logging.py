import time, uuid, logging
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
access_log = logging.getLogger("uvicorn.access")
app_log = logging.getLogger("app")
class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        rid = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        start = time.perf_counter()
        try:
            response: Response = await call_next(request)
            status = response.status_code
        except Exception as e:
            status = 500
            app_log.exception("Unhandled error: %s", e)
            raise
        finally:
            dur_ms = (time.perf_counter() - start) * 1000
            access_log.info('%s %s %s %s %.2fms', request.method, request.url.path,
                            request.query_params._dict if hasattr(request.query_params,"_dict") else str(request.query_params),
                            status, dur_ms)
        if 'X-Request-ID' not in response.headers:
            response.headers['X-Request-ID'] = rid
        return response
