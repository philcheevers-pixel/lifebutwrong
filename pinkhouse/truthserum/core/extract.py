"""Split AI-generated prose into atomic claims."""

from __future__ import annotations

import re

# Sentence-ish boundaries. Keep abbreviations from splitting hard.
_ABBREV = re.compile(
    r"\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|vs|etc|e\.g|i\.e|Fig|Eq|No|Vol|Inc|Ltd|U\.S|U\.K)\.$",
    re.I,
)
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"“‘(])")
_BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")
_WHITESPACE = re.compile(r"\s+")


def _normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u2014", " — ").replace("\u2013", "-")
    return text.strip()


def _split_paragraphs(text: str) -> list[str]:
    parts = re.split(r"\n\s*\n+", text)
    return [p.strip() for p in parts if p.strip()]


def _split_sentences(paragraph: str) -> list[str]:
    lines = []
    for raw_line in paragraph.split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if _BULLET.match(line):
            lines.append(_BULLET.sub("", line).strip())
            continue
        # Soft-split long compounds on semicolons / em dashes when both sides look claim-like.
        chunks = re.split(r"\s*;\s+|\s+—\s+", line)
        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            # Protect common abbreviations before splitting.
            tokens = _SENTENCE_END.split(chunk)
            rebuilt: list[str] = []
            buf = ""
            for tok in tokens:
                candidate = (buf + " " + tok).strip() if buf else tok
                if buf and _ABBREV.search(buf):
                    buf = candidate
                    continue
                if buf:
                    rebuilt.append(buf)
                buf = tok.strip()
            if buf:
                rebuilt.append(buf)
            lines.extend(s for s in rebuilt if s)
    return lines


def _is_claimlike(sentence: str) -> bool:
    words = sentence.split()
    if len(words) < 4:
        return False
    # Drop pure headings / titles in ALL CAPS short lines.
    letters = re.sub(r"[^A-Za-z]", "", sentence)
    if letters and letters.isupper() and len(words) <= 8:
        return False
    # Drop questions that are not assertions (keep rhetorical if long & assertive later).
    if sentence.endswith("?") and len(words) < 12:
        return False
    return True


def extract_claims(text: str, *, max_claims: int = 80) -> list[str]:
    """Return ordered unique claim strings from document text."""
    text = _normalize(text)
    if not text:
        return []

    claims: list[str] = []
    seen: set[str] = set()
    for para in _split_paragraphs(text):
        for sentence in _split_sentences(para):
            cleaned = _WHITESPACE.sub(" ", sentence).strip(" -•*")
            if not _is_claimlike(cleaned):
                continue
            key = cleaned.lower()
            if key in seen:
                continue
            seen.add(key)
            claims.append(cleaned)
            if len(claims) >= max_claims:
                return claims
    return claims
