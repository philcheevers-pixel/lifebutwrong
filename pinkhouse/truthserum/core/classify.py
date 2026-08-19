"""Classify claims into Truth Serum buckets."""

from __future__ import annotations

import re

from .models import Claim, ClaimType

# --- signal patterns ---------------------------------------------------------

URL_RE = re.compile(r"https?://|www\.\w+", re.I)
DOI_RE = re.compile(r"\b10\.\d{4,9}/\S+\b")
CITATION_RE = re.compile(
    r"\b(?:according to|per|cited in|source:|as reported by|see also|"
    r"\(\s*\d{4}\s*\)|et al\.|doi:|pmid|isbn)\b",
    re.I,
)
QUOTE_RE = re.compile(r"[\"'].{8,}[\"']")
HEDGE_RE = re.compile(
    r"\b(?:may|might|could|appears?|seems?|suggests?|indicates?|likely|"
    r"possibly|probably|approximately|roughly|estimated|about)\b",
    re.I,
)
INFER_RE = re.compile(
    r"\b(?:therefore|thus|hence|consequently|so that|this means|"
    r"implies?|implies that|we can conclude|in conclusion)\b",
    re.I,
)
SUPERLATIVE_RE = re.compile(
    r"\b(?:always|never|guaranteed?|proven|definitely|undeniabl\w*|"
    r"100%|perfect(?:ly)?|best|worst|every|no one|everyone|"
    r"impossible|certainly|without (?:any )?doubt)\b",
    re.I,
)
STAT_RE = re.compile(
    r"(?:\d+(?:\.\d+)?\s*%|\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|"
    r"\b(?:million|billion|trillion)\b)",
    re.I,
)
CAUSAL_RE = re.compile(
    r"\b(?:causes?|caused|leads? to|results? in|responsible for|"
    r"due to|because of)\b",
    re.I,
)
MEDICAL_LEGAL_RE = re.compile(
    r"\b(?:cure[sd]?|diagnos(?:e|is|ed)|prescribe|FDA[- ]approved|"
    r"clinically proven|lawsuit|liable|guaranteed refund|"
    r"treat(?:s|ment|ed)? (?:cancer|covid|diabetes))\b",
    re.I,
)
FUTURE_RE = re.compile(
    r"\b(?:will|won't|shall|by 20\d{2}|next year|imminent(?:ly)?|"
    r"inevitable(?:ly)?)\b",
    re.I,
)
FABRICATED_PRECISION_RE = re.compile(
    r"\b\d+\.\d{3,}\b|\b\d{2,}:\d{2}:\d{2}\b"  # over-precise float / fake clock
)
FIRST_PERSON_PROCESS_RE = re.compile(
    r"\b(?:we (?:measured|observed|recorded|tested|found)|"
    r"the (?:document|report|study|data) (?:states?|shows?|indicates?)|"
    r"as (?:shown|stated|described) (?:above|below|herein))\b",
    re.I,
)
DEFINITION_RE = re.compile(
    r"\b(?:is defined as|means that|refers to|consists of|comprises)\b",
    re.I,
)


def _signals(text: str) -> list[str]:
    found: list[str] = []
    checks = [
        ("url", URL_RE),
        ("doi", DOI_RE),
        ("citation", CITATION_RE),
        ("quote", QUOTE_RE),
        ("hedge", HEDGE_RE),
        ("inference", INFER_RE),
        ("superlative", SUPERLATIVE_RE),
        ("statistic", STAT_RE),
        ("causal", CAUSAL_RE),
        ("medical_legal", MEDICAL_LEGAL_RE),
        ("future", FUTURE_RE),
        ("fabricated_precision", FABRICATED_PRECISION_RE),
        ("process", FIRST_PERSON_PROCESS_RE),
        ("definition", DEFINITION_RE),
    ]
    for name, pattern in checks:
        if pattern.search(text):
            found.append(name)
    return found


def classify_claim(text: str) -> Claim:
    """Classify one claim with an explicit reason and signal list."""
    signals = _signals(text)
    has_support = any(s in signals for s in ("url", "doi", "citation", "quote", "process"))

    # Hard problems first.
    if "medical_legal" in signals and not has_support:
        return Claim(
            text=text,
            claim_type=ClaimType.UNVERIFIED,
            reason="Medical/legal assertion without attributable support.",
            signals=signals,
        )
    if "fabricated_precision" in signals and "statistic" in signals and not has_support:
        return Claim(
            text=text,
            claim_type=ClaimType.UNVERIFIED,
            reason="Over-precise numeric claim with no source trail.",
            signals=signals,
        )
    if "superlative" in signals and "statistic" in signals and not has_support:
        return Claim(
            text=text,
            claim_type=ClaimType.UNVERIFIED,
            reason="Absolute/statistical claim presented as fact without evidence.",
            signals=signals,
        )
    if "superlative" in signals and not has_support and "hedge" not in signals:
        return Claim(
            text=text,
            claim_type=ClaimType.WORTH_CHECKING,
            reason="Absolute wording without hedging or citation — verify before sending.",
            signals=signals,
        )
    if "statistic" in signals and not has_support:
        return Claim(
            text=text,
            claim_type=ClaimType.WORTH_CHECKING,
            reason="Numeric claim needs a source before it can be trusted.",
            signals=signals,
        )
    if "causal" in signals and not has_support and "hedge" not in signals:
        return Claim(
            text=text,
            claim_type=ClaimType.WORTH_CHECKING,
            reason="Causal claim without supporting evidence.",
            signals=signals,
        )
    if "future" in signals and "superlative" in signals:
        return Claim(
            text=text,
            claim_type=ClaimType.WORTH_CHECKING,
            reason="Confident future prediction — treat as speculative.",
            signals=signals,
        )

    if "inference" in signals or ("hedge" in signals and not has_support):
        return Claim(
            text=text,
            claim_type=ClaimType.INFERRED,
            reason="Reasonable inference or hedged conclusion; not independently confirmed.",
            signals=signals,
        )

    if has_support or "definition" in signals or "process" in signals:
        return Claim(
            text=text,
            claim_type=ClaimType.OBSERVED,
            reason="Reviewed and found reasonable — support markers or process language present.",
            signals=signals,
        )

    # Default: mild worth-checking for unsupported factual tone.
    if re.search(r"\b(?:is|are|was|were|has|have|will)\b", text) and len(text.split()) >= 8:
        return Claim(
            text=text,
            claim_type=ClaimType.WORTH_CHECKING,
            reason="Factual tone without visible support — spot-check before relying on it.",
            signals=signals,
        )

    return Claim(
        text=text,
        claim_type=ClaimType.INFERRED,
        reason="Soft claim; treated as inferred pending human review.",
        signals=signals,
    )


def classify_claims(texts: list[str]) -> list[Claim]:
    return [classify_claim(t) for t in texts]
