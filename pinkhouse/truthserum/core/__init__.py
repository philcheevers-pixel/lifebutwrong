"""Michelangelo Truth Serum — core package."""

from .models import AnalyzeResponse, ClaimResult, ClaimStatus, Verdict
from .pipeline import analyze_text, analyze_to_dict

__all__ = [
    "AnalyzeResponse",
    "ClaimResult",
    "ClaimStatus",
    "Verdict",
    "analyze_text",
    "analyze_to_dict",
]

__version__ = "0.2.0"
