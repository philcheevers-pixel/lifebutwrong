"""Michelangelo Truth Serum — core audit engine."""

from .audit import audit_text
from .models import AuditResult, Claim, ClaimType
from .report import format_report

__all__ = [
    "Claim",
    "ClaimType",
    "AuditResult",
    "audit_text",
    "format_report",
]

__version__ = "0.1.0"
