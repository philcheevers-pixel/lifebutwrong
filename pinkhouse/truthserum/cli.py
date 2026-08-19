#!/usr/bin/env python3
"""CLI for Michelangelo Truth Serum core audits."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running from package directory without install.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.audit import audit_payload, audit_text  # noqa: E402
from core.report import format_report  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Michelangelo Truth Serum — audit AI text")
    parser.add_argument("path", nargs="?", help="Text file to audit (or stdin)")
    parser.add_argument("--json", action="store_true", help="Emit full JSON payload")
    parser.add_argument("--llm", action="store_true", help="Force LLM refinement")
    parser.add_argument("--no-llm", action="store_true", help="Force heuristic-only")
    args = parser.parse_args(argv)

    if args.path:
        text = Path(args.path).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    use_llm: bool | None
    if args.llm:
        use_llm = True
    elif args.no_llm:
        use_llm = False
    else:
        use_llm = None

    if args.json:
        print(json.dumps(audit_payload(text, use_llm=use_llm), indent=2))
    else:
        result = audit_text(text, use_llm=use_llm)
        report = result.evidence.get("llm_report") or format_report(result)
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
