# Michelangelo Truth Serum — Core Logic

**Brand:** Pink House Technology / Michelangelo only — not Life But Wrong.  
**Live UI:** https://pinkhouse.tech/truth.html  
**Status:** Core audit engine + deploy stubs for the missing `truth-proxy.php` / `truth-pay.php` endpoints (currently 404 on production).

## What this is

Truth Serum audits AI-generated text before someone signs or sends it:

1. Split the document into atomic claims  
2. Classify each claim: **Observed** · **Inferred** · **Worth Checking** · **Unverified**  
3. Compute an interpretable **Trust Score / 100**  
4. Emit a Michelangelo report string the existing frontend already knows how to parse  

Optional: when `ANTHROPIC_API_KEY` is set, the proxy can ask Claude to refine the heuristic pass into a richer report (same wire format).

## Deploy to pinkhouse.tech

Copy these files next to `truth.html` on the Apache docroot:

| File | Role |
|------|------|
| `truth-proxy.php` | POST `{ "text": "..." }` → audit report JSON |
| `truth-pay.php` | Stripe PaymentIntent + coupon bypass |
| `core/` + `truthserum_proxy.py` | Python engine invoked by PHP |

Environment on the server:

```bash
export ANTHROPIC_API_KEY=...          # optional LLM refinement
export TRUTHSERUM_COUPON=TESTFREE     # coupon bypass code
export STRIPE_SECRET_KEY=sk_live_...  # required for real card charges
export TRUTHSERUM_PYTHON=python3
```

Local smoke test (no PHP):

```bash
cd pinkhouse/truthserum
python3 -m tests.test_core
python3 cli.py fixtures/sample_ai_text.txt
python3 truthserum_proxy.py   # http://127.0.0.1:8765/truth-proxy.php
```

## Report wire format (must stay stable)

The live `truth.html` parser expects sections like:

```
PROBLEMS FOUND: N
- ...

WORTH CHECKING: N
- ...

REVIEWED & REASONABLE: N
- ...

TOTAL CLAIMS EXAMINED: N
TRUST SCORE: XX / 100
```

Do not rename those headers without updating the frontend.

## Patent / product context

Provisional patent **63/924,367**. Product page describes Michelangelo as pre-execution governance; Truth Serum is the public claim-audit surface for that framework.
