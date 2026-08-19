"""Data models for Truth Serum audits."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ClaimType(str, Enum):
    """Public Truth Serum claim buckets (UI labels in parentheses)."""

    OBSERVED = "observed"  # Reviewed & Reasonable / Observed
    INFERRED = "inferred"  # Inferred
    WORTH_CHECKING = "speculative"  # Worth Checking (frontend key: speculative)
    UNVERIFIED = "unverified"  # Problems Found / Unverified


@dataclass
class Claim:
    text: str
    claim_type: ClaimType
    reason: str
    signals: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "type": self.claim_type.value,
            "reason": self.reason,
            "signals": list(self.signals),
        }


@dataclass
class AuditResult:
    claims: list[Claim]
    score: int
    recommendation: str
    mode: str = "heuristic"  # heuristic | llm | hybrid
    evidence: dict[str, Any] = field(default_factory=dict)

    @property
    def counts(self) -> dict[str, int]:
        counts = {
            "observed": 0,
            "inferred": 0,
            "speculative": 0,
            "unverified": 0,
            "total": len(self.claims),
        }
        for claim in self.claims:
            key = claim.claim_type.value
            if key == "speculative":
                counts["speculative"] += 1
            elif key in counts:
                counts[key] += 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "recommendation": self.recommendation,
            "mode": self.mode,
            "counts": self.counts,
            "claims": [c.to_dict() for c in self.claims],
            "evidence": self.evidence,
        }

    def as_jsonable(self) -> dict[str, Any]:
        return asdict(self) | {"counts": self.counts, "score": self.score}
