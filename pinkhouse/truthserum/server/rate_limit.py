"""Simple in-memory per-IP daily rate limit."""

from __future__ import annotations

import threading
import time
from collections import defaultdict

from .limits import RATE_LIMIT_PER_DAY

_lock = threading.Lock()
_hits: dict[str, list[float]] = defaultdict(list)


def _prune(bucket: list[float], now: float) -> list[float]:
    day = 86400.0
    return [t for t in bucket if now - t < day]


def check_rate_limit(ip: str) -> tuple[bool, int]:
    """Return (allowed, remaining_after_this_call_if_allowed)."""
    now = time.time()
    with _lock:
        bucket = _prune(_hits.get(ip, []), now)
        if len(bucket) >= RATE_LIMIT_PER_DAY:
            _hits[ip] = bucket
            return False, 0
        bucket.append(now)
        _hits[ip] = bucket
        remaining = max(0, RATE_LIMIT_PER_DAY - len(bucket))
        return True, remaining
