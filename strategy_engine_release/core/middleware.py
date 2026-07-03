"""API request/response logging middleware.

Writes one .txt log file per day inside  strategy_engine_release/logs/
  logs/
    2026-06-04.txt
    2026-06-05.txt
    ...

Each entry format:
  [2026-06-04 09:15:33]  POST  /api/daily-calc  →  200  (3420 ms)
  REQUEST : {"target_date": "2026-06-04", "goal": "work", "energy_level": 7}
  RESPONSE: {"id": 42, "bazi_score": 7.2, ...}
  ────────────────────────────────────────────────────────────────────────────

Skip paths: /docs, /openapi.json, /redoc, /health
"""

import time
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# logs/ folder sits next to main.py  (strategy_engine_release/logs/)
_LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
_LOGS_DIR.mkdir(exist_ok=True)

_SKIP_PREFIXES = ("/docs", "/openapi.json", "/redoc", "/health")
_MAX_BODY_BYTES = 4096  # 4 KB — truncate long bodies


def _decode(raw: bytes) -> str:
    if not raw:
        return "-"
    if len(raw) > _MAX_BODY_BYTES:
        raw = raw[:_MAX_BODY_BYTES] + b" ... [truncated]"
    return raw.decode("utf-8", errors="replace")


def _write_log(now: datetime, method: str, url: str,
               status: int, duration_ms: int,
               req_text: str, resp_text: str) -> None:
    """Append one log entry to logs/YYYY-MM-DD.txt (thread-safe via append mode)."""
    filename = _LOGS_DIR / f"{now.strftime('%Y-%m-%d')}.txt"
    separator = "-" * 76

    entry = (
        f"[{now.strftime('%Y-%m-%d %H:%M:%S')} UTC]  "
        f"{method}  {url}  ->  {status}  ({duration_ms} ms)\n"
        f"REQUEST : {req_text}\n"
        f"RESPONSE: {resp_text}\n"
        f"{separator}\n"
    )

    with open(filename, "a", encoding="utf-8") as f:
        f.write(entry)


class APILoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if any(request.url.path.startswith(p) for p in _SKIP_PREFIXES):
            return await call_next(request)

        t_start = time.perf_counter()

        # Read + re-inject request body so route handlers still receive it
        req_raw = await request.body()
        req_text = _decode(req_raw)

        async def receive():
            return {"type": "http.request", "body": req_raw, "more_body": False}

        request = Request(request.scope, receive)

        # Call actual route
        response = await call_next(request)

        # Buffer response so we can log it, then reconstruct
        resp_chunks: list[bytes] = []
        async for chunk in response.body_iterator:
            resp_chunks.append(chunk)
        resp_raw = b"".join(resp_chunks)
        resp_text = _decode(resp_raw)

        duration_ms = int((time.perf_counter() - t_start) * 1000)
        now = datetime.now(timezone.utc)

        # Write to file — never raise
        try:
            _write_log(
                now=now,
                method=request.method,
                url=str(request.url),
                status=response.status_code,
                duration_ms=duration_ms,
                req_text=req_text,
                resp_text=resp_text,
            )
        except Exception:
            pass

        return Response(
            content=resp_raw,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
