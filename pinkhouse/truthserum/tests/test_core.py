#!/usr/bin/env python3
"""Tests for Truth Serum MVP core."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.extract import extract_claims_heuristic
from core.models import ClaimStatus, Verdict
from core.pipeline import analyze_text
from core.report import compute_verdict
from core.verify import classify_heuristic


class ExtractTests(unittest.TestCase):
    def test_extracts_multiple_claims(self):
        text = (
            "Alpha claim is long enough to count here as one unit. "
            "Beta claim is also long enough to count as another unit.\n\n"
            "- Gamma claim that should be captured from a bullet list item."
        )
        claims = extract_claims_heuristic(text)
        self.assertGreaterEqual(len(claims), 3)


class ClassifyTests(unittest.TestCase):
    def test_supported_with_citation(self):
        c = classify_heuristic(
            "According to FDA guidance, electronic records must remain attributable.",
            "c1",
        )
        self.assertEqual(c.status, ClaimStatus.SUPPORTED)

    def test_unsupported_stat(self):
        c = classify_heuristic(
            "Studies show that 87.3% of quality deviations are caused by AI hallucinations.",
            "c2",
        )
        self.assertEqual(c.status, ClaimStatus.UNSUPPORTED)

    def test_conflation_leap(self):
        c = classify_heuristic(
            "Therefore this clearly proves that every manufacturer will always eliminate all risk.",
            "c3",
        )
        self.assertEqual(c.status, ClaimStatus.CONFLATION)


class PipelineTests(unittest.TestCase):
    def test_sample_fixture(self):
        sample = (ROOT / "fixtures" / "sample_ai_text.txt").read_text(encoding="utf-8")
        result = analyze_text(sample, use_llm=False, use_search=False)
        self.assertIn(result.verdict, {Verdict.GREEN, Verdict.YELLOW, Verdict.RED})
        self.assertGreater(result.claim_count, 0)
        self.assertIn("Truth Serum Report", result.report_markdown)
        self.assertIn("Experimental automated claim review", result.disclaimer)
        self.assertTrue(result.problematic_claims or result.verdict == Verdict.GREEN)
        # Fixture is intentionally messy → not green.
        self.assertNotEqual(result.verdict, Verdict.GREEN)

    def test_verdict_red_on_many_bad(self):
        from core.models import ClaimResult

        claims = [
            ClaimResult(id="1", text="a", status=ClaimStatus.UNSUPPORTED, note="x"),
            ClaimResult(id="2", text="b", status=ClaimStatus.UNSUPPORTED, note="x"),
            ClaimResult(id="3", text="c", status=ClaimStatus.UNSUPPORTED, note="x"),
            ClaimResult(id="4", text="d", status=ClaimStatus.SUPPORTED, note="x"),
        ]
        self.assertEqual(compute_verdict(claims), Verdict.RED)


if __name__ == "__main__":
    unittest.main()
