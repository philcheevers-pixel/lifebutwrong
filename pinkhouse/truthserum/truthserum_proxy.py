#!/usr/bin/env python3
"""
Local / CGI-friendly HTTP front for Truth Serum core.

Mirrors the paths the live truth.html expects:
  POST /truth-proxy.php   { "text": "..." }
  POST /truth-pay.php     { "coupon": "..." }

Production Apache should use the PHP stubs, which shell out to the same engine.
"""

from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.audit import audit_payload  # noqa: E402


def handle_proxy(body: dict) -> tuple[int, dict]:
    text = (body.get("text") or "").strip()
    if not text:
        return 400, {"error": "Missing text"}
    words = text.split()
    if len(words) < 10:
        return 400, {"error": "Please paste at least a few sentences to audit."}
    if len(words) > 10000:
        return 400, {"error": f"Your text is {len(words)} words. Please keep it under 10,000 words."}
    try:
        force = os.environ.get("TRUTHSERUM_FORCE_LLM", "").lower() in {"1", "true", "yes"}
        payload = audit_payload(text, use_llm=True if force else None)
        return 200, payload
    except Exception as exc:  # noqa: BLE001 — surface to client
        return 500, {"error": str(exc)}


def handle_pay(body: dict) -> tuple[int, dict]:
    coupon = (body.get("coupon") or "").strip()
    expected = os.environ.get("TRUTHSERUM_COUPON", "TESTFREE")
    if coupon and coupon == expected:
        return 200, {"coupon_valid": True, "client_secret": "coupon_bypass"}

    secret = os.environ.get("STRIPE_SECRET_KEY", "")
    if not secret:
        return 200, {
            "error": "Stripe is not configured on this server. Use coupon TESTFREE for local testing.",
        }

    # Minimal PaymentIntent create via Stripe API (no SDK dependency).
    import urllib.error
    import urllib.parse
    import urllib.request

    data = urllib.parse.urlencode(
        {
            "amount": "200",  # $2.00 CAD/USD cents — match UI copy
            "currency": os.environ.get("TRUTHSERUM_CURRENCY", "cad"),
            "automatic_payment_methods[enabled]": "true",
            "description": "Michelangelo Truth Serum audit",
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.stripe.com/v1/payment_intents",
        data=data,
        headers={"Authorization": f"Bearer {secret}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            intent = json.loads(resp.read().decode())
        return 200, {"client_secret": intent.get("client_secret")}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return 400, {"error": f"Stripe error: {detail[:300]}"}


class Handler(BaseHTTPRequestHandler):
    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return {}

    def _send(self, code: int, payload: dict) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        body = self._read_json()
        if path.endswith("truth-proxy.php") or path.rstrip("/").endswith("truth-proxy"):
            code, payload = handle_proxy(body)
            self._send(code, payload)
            return
        if path.endswith("truth-pay.php") or path.rstrip("/").endswith("truth-pay"):
            code, payload = handle_pay(body)
            self._send(code, payload)
            return
        self._send(404, {"error": f"Unknown path: {path}"})

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main() -> int:
    host = os.environ.get("TRUTHSERUM_HOST", "127.0.0.1")
    port = int(os.environ.get("TRUTHSERUM_PORT", "8765"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Truth Serum proxy on http://{host}:{port}/truth-proxy.php", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
