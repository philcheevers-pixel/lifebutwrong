"""Word limits, claim caps, and file size guards."""

from __future__ import annotations

import os

MAX_WORDS = int(os.environ.get("TRUTHSERUM_MAX_WORDS", "3000"))
MAX_CLAIMS = int(os.environ.get("TRUTHSERUM_MAX_CLAIMS", "40"))
MAX_UPLOAD_BYTES = int(os.environ.get("TRUTHSERUM_MAX_UPLOAD_BYTES", str(2 * 1024 * 1024)))
RATE_LIMIT_PER_DAY = int(os.environ.get("TRUTHSERUM_RATE_LIMIT_PER_DAY", "5"))


def count_words(text: str) -> int:
    text = text.strip()
    if not text:
        return 0
    return len(text.split())


def enforce_text_limits(text: str) -> str | None:
    """Return error message or None if OK."""
    words = count_words(text)
    if words < 10:
        return "Please provide at least a few sentences to check."
    if words > MAX_WORDS:
        return (
            f"This text is {words:,} words. Truth Serum MVP limit is {MAX_WORDS:,} words. "
            "Trim the document and try again."
        )
    return None
