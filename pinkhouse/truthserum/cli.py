#!/usr/bin/env python3
"""CLI for Truth Serum MVP."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.pipeline import analyze_text  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Truth Serum — experimental claim checker")
    p.add_argument("path", nargs="?", help="Text file (or stdin)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--no-llm", action="store_true")
    p.add_argument("--no-search", action="store_true")
    args = p.parse_args(argv)
    text = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
    result = analyze_text(
        text,
        use_llm=False if args.no_llm else None,
        use_search=False if args.no_search else None,
    )
    if args.json:
        print(json.dumps(result.model_dump(), indent=2))
    else:
        sys.stdout.write(result.report_markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
