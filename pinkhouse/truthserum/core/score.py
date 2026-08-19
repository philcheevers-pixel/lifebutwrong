"""Trust score + recommendation text."""

from __future__ import annotations

from .models import Claim, ClaimType


def recommendation_text(score: int) -> str:
    if score >= 90:
        return "Safe to use. Minor verification only."
    if score >= 70:
        return "Review before relying. Some details should be checked."
    return "Do not send without verification."


def compute_trust_score(claims: list[Claim]) -> int:
    """
    Interpretable score used by Truth Serum UI.

    Penalties (per claim):
      Unverified: -18
      Worth Checking: -8
      Inferred: -2
      Observed: 0

    Bonus: +min(10, observed * 2) when observed claims exist and
    unverified == 0.
    """
    if not claims:
        return 0

    score = 100
    observed = unverified = 0
    for claim in claims:
        if claim.claim_type == ClaimType.UNVERIFIED:
            score -= 18
            unverified += 1
        elif claim.claim_type == ClaimType.WORTH_CHECKING:
            score -= 8
        elif claim.claim_type == ClaimType.INFERRED:
            score -= 2
        elif claim.claim_type == ClaimType.OBSERVED:
            observed += 1

    if observed and unverified == 0:
        score += min(10, observed * 2)

    # Density adjustment: many unsupported claims in a short doc hurt more
    # already via per-claim penalties; clamp to [0, 100].
    return max(0, min(100, int(round(score))))
