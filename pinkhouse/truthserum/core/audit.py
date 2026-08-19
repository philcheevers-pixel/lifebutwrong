"""Orchestrate Truth Serum audit pipeline."""

from __future__ import annotations

import hashlib
import time
from typing import Any

from .classify import classify_claims
from .extract import extract_claims
from .llm import llm_available, refine_with_llm
from .models import AuditResult
from .report import format_report
from .score import compute_trust_score, recommendation_text


def audit_text(
    text: str,
    *,
    use_llm: bool | None = None,
    max_claims: int = 80,
) -> AuditResult:
    """
    Run the Truth Serum core pipeline.

    use_llm:
      None  → use LLM only if ANTHROPIC_API_KEY is present
      True  → require LLM refinement
      False → heuristic only
    """
    started = time.time()
    claims_text = extract_claims(text, max_claims=max_claims)
    claims = classify_claims(claims_text)
    score = compute_trust_score(claims)
    result = AuditResult(
        claims=claims,
        score=score,
        recommendation=recommendation_text(score),
        mode="heuristic",
        evidence={
            "input_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "input_chars": len(text),
            "input_words": len(text.split()),
            "claim_count": len(claims),
            "engine": "truthserum-core",
            "engine_version": "0.1.0",
        },
    )

    want_llm = llm_available() if use_llm is None else use_llm
    if want_llm:
        report = refine_with_llm(text, result)
        # Keep heuristic claims/score as structured truth; attach LLM report
        # for the wire. Re-parse score from LLM when present.
        result.mode = "hybrid"
        result.evidence["llm_report"] = report
        result.evidence["llm_used"] = True
        import re

        m = re.search(r"TRUST SCORE:\s*(\d+)\s*/\s*100", report, re.I)
        if m:
            result.score = max(0, min(100, int(m.group(1))))
            result.recommendation = recommendation_text(result.score)
    else:
        result.evidence["llm_used"] = False

    result.evidence["elapsed_ms"] = int((time.time() - started) * 1000)
    return result


def audit_payload(text: str, *, use_llm: bool | None = None) -> dict[str, Any]:
    """JSON payload matching what truth-proxy.php should return to the UI."""
    result = audit_text(text, use_llm=use_llm)
    report = result.evidence.get("llm_report") or format_report(result)
    return {
        "content": [{"type": "text", "text": report}],
        "text": report,
        "truthserum": result.to_dict(),
    }
