"""Classify and verify claims (heuristic + optional Brave Search + LLM)."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from .models import ClaimResult, ClaimStatus

URL_RE = re.compile(r"https?://|www\.\w+", re.I)
DOI_RE = re.compile(r"\b10\.\d{4,9}/\S+\b")
CITATION_RE = re.compile(
    r"\b(?:according to|per|cited in|source:|as reported by|see also|"
    r"\(\s*\d{4}\s*\)|et al\.|doi:|pmid|isbn)\b",
    re.I,
)
HEDGE_RE = re.compile(
    r"\b(?:may|might|could|appears?|seems?|suggests?|indicates?|likely|"
    r"possibly|probably|approximately|roughly|estimated|about)\b",
    re.I,
)
LEAP_RE = re.compile(
    r"\b(?:therefore|thus|proves?|proof that|means that|so clearly|"
    r"this shows that|obviously|guarantees?)\b",
    re.I,
)
SUPERLATIVE_RE = re.compile(
    r"\b(?:always|never|guaranteed?|definitely|undeniabl\w*|100%|"
    r"perfect(?:ly)?|every|no one|everyone|impossible|without (?:any )?doubt)\b",
    re.I,
)
STAT_RE = re.compile(r"(?:\d+(?:\.\d+)?\s*%|\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b)", re.I)
CAUSAL_RE = re.compile(r"\b(?:causes?|caused|leads? to|results? in|responsible for)\b", re.I)
MEDICAL_RE = re.compile(
    r"\b(?:cure[sd]?|diagnos(?:e|is|ed)|clinically proven|"
    r"treat(?:s|ment|ed)? (?:cancer|covid|diabetes))\b",
    re.I,
)
PROCESS_RE = re.compile(
    r"\b(?:we (?:measured|observed|recorded|tested|found)|"
    r"the (?:document|report|study|data) (?:states?|shows?|indicates?)|"
    r"as (?:shown|stated|described) (?:above|below|herein))\b",
    re.I,
)


def classify_heuristic(text: str, claim_id: str) -> ClaimResult:
    has_support = bool(
        URL_RE.search(text)
        or DOI_RE.search(text)
        or CITATION_RE.search(text)
        or PROCESS_RE.search(text)
    )
    hedge = bool(HEDGE_RE.search(text))
    leap = bool(LEAP_RE.search(text))
    absolute = bool(SUPERLATIVE_RE.search(text))
    stat = bool(STAT_RE.search(text))
    causal = bool(CAUSAL_RE.search(text))
    medical = bool(MEDICAL_RE.search(text))

    if medical and not has_support:
        return ClaimResult(
            id=claim_id,
            text=text,
            status=ClaimStatus.UNSUPPORTED,
            note="Medical-style assertion without attributable support.",
        )
    if absolute and stat and not has_support:
        return ClaimResult(
            id=claim_id,
            text=text,
            status=ClaimStatus.UNSUPPORTED,
            note="Absolute/statistical claim presented as fact without evidence.",
        )
    if leap and (absolute or causal) and not has_support:
        return ClaimResult(
            id=claim_id,
            text=text,
            status=ClaimStatus.CONFLATION,
            note="Possible leap — conclusion is stronger than the support shown.",
        )
    if leap and not has_support:
        return ClaimResult(
            id=claim_id,
            text=text,
            status=ClaimStatus.CONFLATION,
            note="Inference marker without clear grounding — check the jump.",
        )
    if (stat or causal or absolute) and not has_support:
        return ClaimResult(
            id=claim_id,
            text=text,
            status=ClaimStatus.UNSUPPORTED,
            note="Needs a source or clearer grounding before relying on it.",
        )
    if not has_support and not hedge and len(text.split()) >= 10:
        return ClaimResult(
            id=claim_id,
            text=text,
            status=ClaimStatus.UNCLEAR,
            note="Factual tone without visible support — needs more context.",
        )
    if has_support or hedge:
        return ClaimResult(
            id=claim_id,
            text=text,
            status=ClaimStatus.SUPPORTED,
            note="Looks supported or carefully hedged on the face of the text.",
        )
    return ClaimResult(
        id=claim_id,
        text=text,
        status=ClaimStatus.UNCLEAR,
        note="Not enough signal to judge — needs more context.",
    )


def brave_search(query: str, *, count: int = 3) -> list[dict]:
    api_key = os.environ.get("BRAVE_API_KEY") or os.environ.get("BRAVE_SEARCH_API_KEY")
    if not api_key:
        return []
    params = urllib.parse.urlencode({"q": query[:400], "count": str(count)})
    req = urllib.request.Request(
        f"https://api.search.brave.com/res/v1/web/search?{params}",
        headers={
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
        return []
    results = []
    for item in (data.get("web") or {}).get("results") or []:
        results.append(
            {
                "title": item.get("title") or "",
                "url": item.get("url") or "",
                "description": item.get("description") or "",
            }
        )
    return results


_JUDGE_SYSTEM = """You verify one claim for Truth Serum using the provided search snippets.
Return ONLY JSON:
{"status":"supported|unsupported|unclear|conflation","note":"one short plain-language sentence","evidence":["url or title", "..."]}
Rules:
- supported = snippets clearly back the claim
- unsupported = claim conflicts with snippets or has no backing for a strong factual assertion
- unclear = not enough information
- conflation = mixes ideas / overclaims relative to evidence
- Be concise. Do not invent sources.
"""


def llm_judge(claim: str, snippets: list[dict]) -> Optional[ClaimResult]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    model = os.environ.get("TRUTHSERUM_MODEL", "claude-sonnet-4-20250514")
    snip_text = "\n".join(
        f"- {s.get('title')}: {s.get('description')} ({s.get('url')})" for s in snippets
    ) or "(no search results)"
    payload = {
        "model": model,
        "max_tokens": 400,
        "system": _JUDGE_SYSTEM,
        "messages": [
            {
                "role": "user",
                "content": f"Claim:\n{claim}\n\nSearch snippets:\n{snip_text}",
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
        with urllib.request.urlopen(req, timeout=45) as resp:
            body = json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
        return None
    parts = [p.get("text", "") for p in body.get("content", []) if p.get("type") == "text"]
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", "\n".join(parts).strip()).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    status_raw = str(data.get("status", "unclear")).lower().strip()
    mapping = {
        "supported": ClaimStatus.SUPPORTED,
        "unsupported": ClaimStatus.UNSUPPORTED,
        "weakly_supported": ClaimStatus.UNSUPPORTED,
        "unclear": ClaimStatus.UNCLEAR,
        "conflation": ClaimStatus.CONFLATION,
        "leap": ClaimStatus.CONFLATION,
    }
    status = mapping.get(status_raw, ClaimStatus.UNCLEAR)
    note = str(data.get("note") or "Judged by model with available evidence.").strip()
    evidence = [str(e) for e in (data.get("evidence") or []) if e][:5]
    return ClaimResult(id="tmp", text=claim, status=status, note=note, evidence=evidence)


def verify_claim(text: str, claim_id: str, *, use_search: bool = True, use_llm: bool = True) -> ClaimResult:
    base = classify_heuristic(text, claim_id)
    snippets: list[dict] = []
    if use_search:
        snippets = brave_search(text)
        if snippets:
            base.evidence = [s.get("url") or s.get("title") or "" for s in snippets if s][:3]

    if use_llm and (snippets or os.environ.get("TRUTHSERUM_LLM_WITHOUT_SEARCH") == "1"):
        judged = llm_judge(text, snippets)
        if judged:
            judged.id = claim_id
            if not judged.evidence and snippets:
                judged.evidence = [s.get("url") or s.get("title") or "" for s in snippets][:3]
            return judged

    if snippets and base.status == ClaimStatus.UNCLEAR:
        # Soft bump: search found something but no LLM — mark as needing human check still
        base.note = "Search returned related pages; manual check still recommended."
    return base
