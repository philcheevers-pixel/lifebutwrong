"""Format Michelangelo report text for truth.html parser."""

from __future__ import annotations

from .models import AuditResult, ClaimType


SECTION_ORDER = (
    (ClaimType.UNVERIFIED, "PROBLEMS FOUND"),
    (ClaimType.WORTH_CHECKING, "WORTH CHECKING"),
    (ClaimType.OBSERVED, "REVIEWED & REASONABLE"),
)


def format_report(result: AuditResult) -> str:
    """
    Produce the exact section headers the live frontend parses.

    Note: Inferred claims are included under WORTH CHECKING when no
    dedicated 'INFERRED' section exists in the wire format, OR listed
    after REVIEWED if we choose to keep them visible. The UI has an
    Inferred counter; we expose inferred via counts and also list them
    in a trailing INFERRED section that the parser maps to 'inferred'
    only if we add that — current parser only knows three sections.

    Strategy compatible with today's truth.html:
      - PROBLEMS FOUND ← unverified
      - WORTH CHECKING ← worth_checking + inferred (inferred are softer)
      - REVIEWED & REASONABLE ← observed
    And set inferred count in structured JSON separately.
    """
    by_type: dict[ClaimType, list[str]] = {
        ClaimType.UNVERIFIED: [],
        ClaimType.WORTH_CHECKING: [],
        ClaimType.INFERRED: [],
        ClaimType.OBSERVED: [],
    }
    for claim in result.claims:
        by_type[claim.claim_type].append(claim.text)

    problems = by_type[ClaimType.UNVERIFIED]
    # Frontend WORTH CHECKING bucket = speculative; include inferred bullets
    # so they remain human-visible in the report body.
    worth = by_type[ClaimType.WORTH_CHECKING] + by_type[ClaimType.INFERRED]
    reviewed = by_type[ClaimType.OBSERVED]

    lines: list[str] = ["ANALYSIS SUMMARY", ""]
    lines.append(f"PROBLEMS FOUND: {len(problems)}")
    for item in problems:
        lines.append(f"- {item}")
    lines.append("")
    lines.append(f"WORTH CHECKING: {len(worth)}")
    for item in worth:
        lines.append(f"- {item}")
    lines.append("")
    lines.append(f"REVIEWED & REASONABLE: {len(reviewed)}")
    for item in reviewed:
        lines.append(f"- {item}")
    lines.append("")
    lines.append(f"TOTAL CLAIMS EXAMINED: {len(result.claims)}")
    lines.append(f"TRUST SCORE: {result.score} / 100")
    lines.append(f"RECOMMENDATION: {result.recommendation}")
    if result.mode != "heuristic":
        lines.append(f"MODE: {result.mode}")
    return "\n".join(lines).strip() + "\n"
