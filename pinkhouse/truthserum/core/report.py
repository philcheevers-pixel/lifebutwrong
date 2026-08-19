"""Report generation and overall verdict."""

from __future__ import annotations

import html

from .models import (
    DISCLAIMER,
    STATUS_LABELS,
    VERDICT_SENTENCES,
    AnalyzeResponse,
    ClaimResult,
    ClaimStatus,
    Verdict,
)


def breakdown(claims: list[ClaimResult]) -> dict[str, int]:
    counts = {s.value: 0 for s in ClaimStatus}
    for c in claims:
        counts[c.status.value] += 1
    return counts


def compute_verdict(claims: list[ClaimResult]) -> Verdict:
    if not claims:
        return Verdict.YELLOW
    counts = breakdown(claims)
    bad = counts[ClaimStatus.UNSUPPORTED.value] + counts[ClaimStatus.CONFLATION.value]
    unclear = counts[ClaimStatus.UNCLEAR.value]
    total = len(claims)
    if bad >= max(2, total * 0.25) or counts[ClaimStatus.UNSUPPORTED.value] >= 3:
        return Verdict.RED
    if bad >= 1 or unclear >= max(2, total * 0.35):
        return Verdict.YELLOW
    return Verdict.GREEN


def problematic(claims: list[ClaimResult]) -> list[ClaimResult]:
    return [c for c in claims if c.status != ClaimStatus.SUPPORTED]


def render_markdown(result: AnalyzeResponse) -> str:
    lines = [
        "# Truth Serum Report",
        "",
        f"> {DISCLAIMER}",
        "",
        f"**Verdict:** {result.verdict.value.upper()} — {result.summary}",
        "",
        f"**Claims extracted:** {result.claim_count}",
        "",
        "## Breakdown",
        "",
    ]
    for status in ClaimStatus:
        lines.append(f"- {STATUS_LABELS[status]}: {result.breakdown.get(status.value, 0)}")
    lines += ["", "## Issues to review", ""]
    focus = result.problematic_claims or []
    if not focus:
        lines.append("No problematic claims flagged.")
    else:
        for c in focus:
            lines.append(f"### {STATUS_LABELS[c.status]}")
            lines.append(f"- **Claim:** {c.text}")
            lines.append(f"- **Note:** {c.note}")
            if c.evidence:
                lines.append(f"- **Evidence:** {'; '.join(c.evidence)}")
            lines.append("")
    lines += ["", "---", "", DISCLAIMER, ""]
    return "\n".join(lines)


def render_html(result: AnalyzeResponse) -> str:
    color = {"green": "#1e8449", "yellow": "#d4ac0d", "red": "#c0392b"}[result.verdict.value]
    items = []
    focus = result.problematic_claims or []
    if not focus:
        items.append("<p>No problematic claims flagged.</p>")
    else:
        for c in focus:
            ev = ""
            if c.evidence:
                ev = "<ul>" + "".join(f"<li>{html.escape(e)}</li>" for e in c.evidence) + "</ul>"
            items.append(
                f"<article class='claim'><h3>{html.escape(STATUS_LABELS[c.status])}</h3>"
                f"<p><strong>Claim:</strong> {html.escape(c.text)}</p>"
                f"<p><strong>Note:</strong> {html.escape(c.note)}</p>{ev}</article>"
            )
    breakdown_rows = "".join(
        f"<li>{html.escape(STATUS_LABELS[s])}: {result.breakdown.get(s.value, 0)}</li>"
        for s in ClaimStatus
    )
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Truth Serum Report</title>
<style>
body{{font-family:Georgia,serif;max-width:720px;margin:2rem auto;padding:0 1rem;color:#111;background:#f7f4ef}}
.verdict{{font-size:1.4rem;font-weight:700;color:{color}}}
.disclaimer{{font-size:.9rem;color:#555;border-left:3px solid #999;padding-left:.75rem;margin:1rem 0}}
.claim{{background:#fff;border:1px solid #ddd;padding:1rem;margin:1rem 0}}
</style></head><body>
<p class="disclaimer">{html.escape(DISCLAIMER)}</p>
<p class="verdict">{result.verdict.value.upper()} — {html.escape(result.summary)}</p>
<p>Claims extracted: {result.claim_count}</p>
<h2>Breakdown</h2><ul>{breakdown_rows}</ul>
<h2>Issues to review</h2>
{''.join(items)}
<p class="disclaimer">{html.escape(DISCLAIMER)}</p>
</body></html>
"""


def attach_reports(result: AnalyzeResponse) -> AnalyzeResponse:
    result.report_markdown = render_markdown(result)
    result.report_html = render_html(result)
    return result


def summary_for(verdict: Verdict) -> str:
    return VERDICT_SENTENCES[verdict]
