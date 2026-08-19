"""Data models for Truth Serum MVP."""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ClaimStatus(str, Enum):
    SUPPORTED = "supported"
    UNSUPPORTED = "unsupported"  # Unsupported / weakly supported
    UNCLEAR = "unclear"  # Needs more context
    CONFLATION = "conflation"  # Possible conflation or leap


class Verdict(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class ClaimResult(BaseModel):
    id: str
    text: str
    status: ClaimStatus
    note: str
    evidence: list[str] = Field(default_factory=list)
    excerpt: Optional[str] = None


class AnalyzeResponse(BaseModel):
    verdict: Verdict
    summary: str
    claim_count: int
    breakdown: dict[str, int]
    claims: list[ClaimResult]
    problematic_claims: list[ClaimResult]
    disclaimer: str
    mode: str  # heuristic | search | llm | hybrid
    limits: dict[str, Any] = Field(default_factory=dict)
    report_markdown: str = ""
    report_html: str = ""


DISCLAIMER = (
    "Experimental automated claim review. Not a substitute for expert fact-checking. "
    "Built to surface issues, not to rubber-stamp documents."
)

STATUS_LABELS = {
    ClaimStatus.SUPPORTED: "Supported",
    ClaimStatus.UNSUPPORTED: "Unsupported / weakly supported",
    ClaimStatus.UNCLEAR: "Unclear / needs more context",
    ClaimStatus.CONFLATION: "Possible conflation or leap",
}

VERDICT_SENTENCES = {
    Verdict.GREEN: "Most extracted claims look supported or carefully hedged.",
    Verdict.YELLOW: "Some claims need checking before you rely on this text.",
    Verdict.RED: "Material unsupported or conflated claims were found — do not treat this as clean.",
}
