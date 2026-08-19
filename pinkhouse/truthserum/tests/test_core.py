#!/usr/bin/env python3
"""Unit tests for Michelangelo Truth Serum core logic."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.audit import audit_payload, audit_text
from core.classify import classify_claim
from core.extract import extract_claims
from core.models import ClaimType
from core.report import format_report
from core.score import compute_trust_score, recommendation_text


class ExtractTests(unittest.TestCase):
    def test_splits_sentences_and_bullets(self):
        text = (
            "Alpha statement is long enough here. Beta statement is also long enough.\n\n"
            "- Gamma claim that should be captured as a bullet claim."
        )
        claims = extract_claims(text)
        self.assertGreaterEqual(len(claims), 3)
        self.assertTrue(any("Gamma" in c for c in claims))


class ClassifyTests(unittest.TestCase):
    def test_sourced_claim_is_observed(self):
        claim = classify_claim(
            "According to FDA guidance, electronic records must remain attributable."
        )
        self.assertEqual(claim.claim_type, ClaimType.OBSERVED)

    def test_stat_without_source_is_worth_checking_or_unverified(self):
        claim = classify_claim(
            "Studies show that 87.3% of quality deviations are caused by AI hallucinations."
        )
        self.assertIn(
            claim.claim_type,
            {ClaimType.WORTH_CHECKING, ClaimType.UNVERIFIED},
        )

    def test_medical_absolute_is_unverified(self):
        claim = classify_claim(
            "This treatment is clinically proven and guaranteed to cure diabetes in all patients."
        )
        self.assertEqual(claim.claim_type, ClaimType.UNVERIFIED)

    def test_inference_marker(self):
        claim = classify_claim(
            "Therefore organizations that deploy runtime governance appear more inspection-ready."
        )
        self.assertEqual(claim.claim_type, ClaimType.INFERRED)


class ScoreTests(unittest.TestCase):
    def test_empty_is_zero(self):
        self.assertEqual(compute_trust_score([]), 0)

    def test_recommendation_bands(self):
        self.assertIn("Safe", recommendation_text(95))
        self.assertIn("Review", recommendation_text(75))
        self.assertIn("Do not send", recommendation_text(20))


class AuditIntegrationTests(unittest.TestCase):
    def test_sample_fixture_produces_parseable_report(self):
        sample = (ROOT / "fixtures" / "sample_ai_text.txt").read_text(encoding="utf-8")
        result = audit_text(sample, use_llm=False)
        report = format_report(result)
        self.assertIn("PROBLEMS FOUND:", report)
        self.assertIn("WORTH CHECKING:", report)
        self.assertIn("REVIEWED & REASONABLE:", report)
        self.assertIn("TOTAL CLAIMS EXAMINED:", report)
        self.assertRegex(report, r"TRUST SCORE:\s*\d+\s*/\s*100")
        self.assertGreater(result.counts["total"], 0)
        # Sample contains unsupported stats / absolutes → not a perfect score.
        self.assertLess(result.score, 100)

    def test_payload_shape_matches_frontend(self):
        sample = (ROOT / "fixtures" / "sample_ai_text.txt").read_text(encoding="utf-8")
        payload = audit_payload(sample, use_llm=False)
        self.assertIn("content", payload)
        self.assertEqual(payload["content"][0]["type"], "text")
        self.assertTrue(payload["content"][0]["text"])
        self.assertIn("truthserum", payload)
        self.assertIn("score", payload["truthserum"])


if __name__ == "__main__":
    unittest.main()
