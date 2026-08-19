"""Truth Serum end-to-end pipeline."""

from __future__ import annotations

import os
from typing import Any

from .extract import extract_claims
from .models import DISCLAIMER, AnalyzeResponse, ClaimResult
from .report import attach_reports, breakdown, compute_verdict, problematic, summary_for
from .verify import verify_claim


def analyze_text(
    text: str,
    *,
    max_claims: int | None = None,
    use_search: bool | None = None,
    use_llm: bool | None = None,
) -> AnalyzeResponse:
    max_claims = max_claims or int(os.environ.get("TRUTHSERUM_MAX_CLAIMS", "40"))
    if use_search is None:
        use_search = bool(os.environ.get("BRAVE_API_KEY") or os.environ.get("BRAVE_SEARCH_API_KEY"))
    if use_llm is None:
        use_llm = bool(os.environ.get("ANTHROPIC_API_KEY"))

    claims_text, extract_mode = extract_claims(
        text, max_claims=max_claims, prefer_llm=use_llm
    )
    results: list[ClaimResult] = []
    for i, claim in enumerate(claims_text, start=1):
        results.append(
            verify_claim(
                claim,
                f"c{i}",
                use_search=use_search,
                use_llm=use_llm,
            )
        )

    verdict = compute_verdict(results)
    modes = [extract_mode]
    if use_search:
        modes.append("search")
    if use_llm:
        modes.append("llm")
    mode = "+".join(dict.fromkeys(modes))  # unique, ordered

    response = AnalyzeResponse(
        verdict=verdict,
        summary=summary_for(verdict),
        claim_count=len(results),
        breakdown=breakdown(results),
        claims=results,
        problematic_claims=problematic(results),
        disclaimer=DISCLAIMER,
        mode=mode,
        limits={
            "max_claims": max_claims,
            "claims_returned": len(results),
        },
    )
    return attach_reports(response)


def analyze_to_dict(text: str, **kwargs: Any) -> dict:
    return analyze_text(text, **kwargs).model_dump()
