"""Optional Anthropic refinement for Truth Serum audits."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from .models import AuditResult
from .report import format_report

SYSTEM_PROMPT = """You are Michelangelo Truth Serum, an AI-output audit engine for Pink House Technology.
You receive a document and a heuristic pre-audit. Refine the audit.

Return ONLY a report with these exact headers (keep names identical):

ANALYSIS SUMMARY

PROBLEMS FOUND: <n>
- <claim>

WORTH CHECKING: <n>
- <claim>

REVIEWED & REASONABLE: <n>
- <claim>

TOTAL CLAIMS EXAMINED: <n>
TRUST SCORE: <0-100> / 100

Rules:
- PROBLEMS FOUND = unverified / no basis / fabricated-sounding assertions
- WORTH CHECKING = possible issue or missing support
- REVIEWED & REASONABLE = verifiable or carefully hedged / sourced claims
- Be strict on statistics, medical/legal claims, and absolute language without sources
- Do not invent quotes or sources that are not in the document
- Prefer fewer, sharper bullets over dumping every sentence
"""


def llm_available() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def refine_with_llm(text: str, heuristic: AuditResult, *, model: str | None = None) -> str:
    """Call Anthropic Messages API; return raw report text."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")

    model = model or os.environ.get("TRUTHSERUM_MODEL", "claude-sonnet-4-20250514")
    pre = format_report(heuristic)
    user = (
        "Document to audit:\n"
        "---\n"
        f"{text[:50000]}\n"
        "---\n\n"
        "Heuristic pre-audit (may refine, do not ignore clear problems):\n"
        f"{pre}\n"
    )
    payload: dict[str, Any] = {
        "model": model,
        "max_tokens": 4096,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": user}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Anthropic HTTP {exc.code}: {detail[:400]}") from exc

    parts = body.get("content") or []
    texts = [p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text"]
    report = "\n".join(t for t in texts if t).strip()
    if not report:
        raise RuntimeError("Empty LLM audit response")
    return report
