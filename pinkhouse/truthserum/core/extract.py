"""Extract atomic, checkable claims from prose."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Optional

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


def _is_claimlike(sentence: str) -> bool:
    words = sentence.split()
    if len(words) < 5:
        return False
    letters = re.sub(r"[^A-Za-z]", "", sentence)
    if letters and letters.isupper() and len(words) <= 8:
        return False
    if sentence.endswith("?") and len(words) < 14:
        return False
    # Skip pure imperatives / UI chrome
    if re.match(r"^(click|tap|press|download|subscribe)\b", sentence, re.I):
        return False
    return True


def extract_claims_heuristic(text: str, *, max_claims: int = 40) -> list[str]:
    text = _normalize(text)
    if not text:
        return []
    claims: list[str] = []
    seen: set[str] = set()
    for para in re.split(r"\n\s*\n+", text):
        for raw_line in para.split("\n"):
            line = raw_line.strip()
            if not line:
                continue
            if _BULLET.match(line):
                pieces = [_BULLET.sub("", line).strip()]
            else:
                pieces = re.split(r"\s*;\s+|\s+—\s+", line)
            for piece in pieces:
                piece = piece.strip()
                if not piece:
                    continue
                # Sentence split with abbrev guard
                parts = _SENTENCE_END.split(piece)
                buf = ""
                sentences: list[str] = []
                for tok in parts:
                    candidate = (buf + " " + tok).strip() if buf else tok
                    if buf and _ABBREV.search(buf):
                        buf = candidate
                        continue
                    if buf:
                        sentences.append(buf)
                    buf = tok.strip()
                if buf:
                    sentences.append(buf)
                for sentence in sentences:
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


_LLM_EXTRACT_SYSTEM = """You extract discrete, checkable claims from text for Truth Serum.
Return ONLY a JSON array of strings. Each string is one atomic claim.
Rules:
- Prefer factual assertions that can be checked.
- Skip pure opinion fluff, greetings, and instructions.
- Keep claims short and self-contained.
- Max claims as instructed.
- No markdown, no commentary — JSON array only.
"""


def extract_claims_llm(text: str, *, max_claims: int = 40) -> Optional[list[str]]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    model = os.environ.get("TRUTHSERUM_MODEL", "claude-sonnet-4-20250514")
    payload = {
        "model": model,
        "max_tokens": 2048,
        "system": _LLM_EXTRACT_SYSTEM,
        "messages": [
            {
                "role": "user",
                "content": f"Extract up to {max_claims} claims from:\n---\n{text[:40000]}\n---",
            }
        ],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
        return None
    parts = [p.get("text", "") for p in body.get("content", []) if p.get("type") == "text"]
    raw = "\n".join(parts).strip()
    # Strip code fences if present
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, list):
        return None
    out: list[str] = []
    seen: set[str] = set()
    for item in data:
        if not isinstance(item, str):
            continue
        cleaned = _WHITESPACE.sub(" ", item).strip()
        if len(cleaned.split()) < 4:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
        if len(out) >= max_claims:
            break
    return out or None


def extract_claims(text: str, *, max_claims: int = 40, prefer_llm: bool = True) -> tuple[list[str], str]:
    """Return (claims, extract_mode)."""
    if prefer_llm:
        llm = extract_claims_llm(text, max_claims=max_claims)
        if llm:
            return llm, "llm"
    return extract_claims_heuristic(text, max_claims=max_claims), "heuristic"
