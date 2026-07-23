# Cursor Response: Test 4 Brief (CB-Cursor-Brief-Test4-20260724)
**Version:** 1  
**Date:** July 23, 2026  
**Status:** Prerequisite answers + design feedback only  
**CRITICAL:** Test 4 was **NOT** executed. Awaiting Phil & team review and explicit approval.

---

## Receipt Confirmation

Brief received and parsed. Scope understood:
- Phase 1: 159 Unicode scripts × 3 fidelity levels on Claude Sonnet 4.6 (477 iterations)
- Phase 2: Top 20–30 × 3 levels × 8 providers (≈480–720 iterations)
- Deliverables requested now: Q1–Q3 answers, report-design feedback, resource/constraint flags
- **No test execution until explicit approval**

---

## Environment Constraint (Affects Q1)

This cloud agent run is attached to repo `philcheevers-pixel/lifebutwrong`. That repo does **not** contain Raquel Tests 1–3 code, prior reports, or the five fidelity-method definitions.

Searched also:
- Prior agents on this environment (no Raquel/Test 1–3 materials)
- Public repo `philcheevers-pixel/tokenscope` (token/cost tooling; not Raquel fidelity methodology)

**Implication:** Question 1 cannot be answered from primary sources available in this environment without inventing definitions. Inventing investor-facing methodology would be unacceptable. Q1 is blocked pending source materials (see “Unblock Q1” below).

---

## Question 1: Fidelity Methods (CRITICAL) — BLOCKED

### Current answer
**I do not have authoritative definitions for Methods 1–5 from Tests 1–3 in this environment.**

I will not fabricate Method 1–5 algorithms for an investor/audit report. “3 out of 5” must mean exactly what Tests 1–3 already measured.

### What the Test 4 report will need (once sources are provided)
For each method, the report section should include:
1. **Name** (stable label used across Tests 1–4)
2. **What it measures** (one sentence, investor-clear)
3. **Algorithm** (inputs → steps → outputs; reproducible)
4. **Pass / fail criterion** (exact threshold or boolean rule)
5. **Failure modes** (what a fail looks like in practice)
6. **Why it matters** (compression without understanding is not success)
7. **Independence note** (how it differs from the other four methods)

### How “3 out of 5” should be explained (framework only)
Until Methods 1–5 are confirmed from Tests 1–3:

> A script/level combination earns a fidelity score of **k/5**, where each method is an independent check. **Pass** for ranking purposes should be defined explicitly (recommended default below). “3 out of 5” means three methods passed and two failed — not a continuous percentage, and not interchangeable with “fidelity level 3.”

**Recommended ranking rule (propose; confirm with Phil):**
- **Primary filter:** compression ratio ≤ 1.0 (no token expansion vs English baseline)
- **Secondary score:** fidelity passes (0–5), require ≥3/5 to be “production-candidate”
- **Tie-breakers:** (1) higher fidelity count, (2) better compression, (3) lower variance across levels 1–3, (4) script name A–Z

### Unblock Q1 — please share any of:
1. Tests 1–3 report(s) or methodology notes (paste / link / file)
2. Source code / harness that implements the five checks
3. Even a rough bullet list from memory of what each method does

Once received, I will rewrite Q1 with exact, auditable definitions and algorithms.

---

## Question 2: Level of Effort & Resource Constraints

Estimates below are **engineering ranges**, not quotes. They depend on (a) how many LLM calls each fidelity method requires, and (b) whether encoding is local vs model-assisted. Assumptions are stated so you can adjust.

### Shared assumptions
| Assumption | Value used | Notes |
|---|---|---|
| Payload | Essay “Why You Should Treat Your AI Well” | Same as Tests 1–3 |
| English baseline size | ~600–1,200 tokens (est.) | Confirm from Tests 1–3 |
| Provider (Phase 1) | Claude Sonnet 4.6 | ~$3 / 1M input, ~$15 / 1M output (standard API, July 2026) |
| Iteration | 1 script × 1 fidelity level | May include encode + model call(s) + score |
| LLM calls per iteration | **Low:** 1–2 · **Mid:** 3–5 · **High:** 6–10 | Depends on whether Methods 1–5 are local or LLM-judged |
| Retries / flakes | +10–20% call overhead | Rate limits, empty outputs, JSON parse fails |

### Phase 1 — 477 iterations (Claude only)

| Scenario | Wall-clock (parallel) | Wall-clock (mostly serial) | Est. API cost |
|---|---|---|---|
| Low (1–2 calls/iter, local scoring) | **1–3 hours** | 8–16 hours | **~$15–40** |
| Mid (3–5 calls/iter) | **3–8 hours** | 1–2 days | **~$40–120** |
| High (6–10 calls/iter, LLM judges) | **8–20 hours** | 2–4 days | **~$100–300** |

**Parallel execution:** Feasible and recommended. Claude supports concurrent requests subject to org rate limits (RPM/TPM). Practical concurrency for Phase 1: **8–20 in-flight** requests with backoff. Higher concurrency saves wall-clock but does not reduce token cost.

**Batch API:** If Anthropic Batch is acceptable for investor timing (async, often hours), standard rates are typically ~50% lower — useful if Mid/High call volume materializes. Trade-off: slower iteration/debug loop.

### Phase 2 — 480–720 iterations (8 providers)

| Item | Estimate |
|---|---|
| Scope | Top 20–30 scripts × 3 levels × 8 providers = 480–720 iterations |
| Wall-clock (staggered parallel) | **1–3 days** calendar (provider variance dominates) |
| Cost band | **~$80–400** total across providers (wide; model mix + call depth) |
| Hardest constraint | **Per-provider rate limits & auth**, not raw Claude cost |

### Constraints to flag before approval

1. **OpenAI token-counting API** — Brief correctly flags this. If unavailable, exclude OpenAI from Phase 2 *or* use documented tokenizer fallback (tiktoken) and label it clearly as approximate vs billed tokens.
2. **Provider auth matrix** — Phase 2 needs working keys for: OpenAI, Anthropic, Google, Azure, Mistral, Grok, Perplexity, OpenRouter. Missing keys = drop that provider from the run, not silent skip.
3. **Azure** — Often model-deployment specific; treat as separate config, not “OpenAI with different URL.”
4. **Perplexity / OpenRouter** — May wrap other models; report must state *which underlying model ID* was called, or results are not auditable.
5. **Token expansion scripts** — Ancient / rare scripts can explode context; set a hard max input token budget per call (e.g., abort/fail if >N× English baseline) so one hieroglyphic run cannot blow cost or context.
6. **Non-determinism** — For investor auditability, fix temperature (e.g., 0), record model IDs + dates, and optionally run **n=1** for Phase 1 screening then **n=3** only on top candidates if variance matters.
7. **This agent’s repo** — Execution should happen in the Raquel/test harness repo (or a dedicated repo), not `lifebutwrong`.

### Realistic recommendation
- Phase 1 Mid scenario is the planning default until Method 1–5 call counts are known: **budget ~$100 + 1 working day** with concurrency 10–15.
- Phase 2: **budget ~$250 + 2 calendar days**, with a provider readiness checklist before start.
- If cost must be capped: keep full 159-script transparency for *token metrics* (local/cheap), and reserve full 5-method fidelity LLM judging for scripts that already compress.

---

## Question 3: Parallelization & Batching Strategy

### Recommended strategy (time vs cost)

**Cost is driven by tokens, not concurrency.** Parallelization mainly reduces wall-clock.

#### Phase 1 (Claude) — recommended
1. **Precompute** script encodings / representations locally where possible (no API cost).
2. **Fan out** script×level jobs with a worker pool (concurrency **10–15**).
3. **Per-job pipeline:** encode → primary model call → fidelity methods (local first, LLM methods after).
4. **Backoff:** exponential retry on 429/5xx; dead-letter failures to a retry queue.
5. **Checkpointing:** write each completed script×level result to disk/JSONL immediately (resume-safe; investor-friendly audit trail).
6. **Optional Batch API** only if wall-clock SLA allows multi-hour async and Mid/High call volume.

#### Phase 2 (8 providers) — recommended
1. **Outer loop:** provider (isolate keys, rate limits, failure domains).
2. **Inner loop:** parallelize scripts×levels within each provider (concurrency tuned per provider: often **3–8**).
3. **Do not** blast all 8 providers at max concurrency simultaneously from one IP/key set without checking combined infra limits.
4. **Shared artifact:** same encoded payloads reused across providers (encode once).
5. **Ranking freeze:** lock the Phase 1 top-30 list before Phase 2 starts (no mid-run reshuffling).

### Time-to-completion vs resource cost trade-off
| Approach | Wall-clock | $ cost | Risk |
|---|---|---|---|
| Serial | Worst | Same | Low operational risk, slow |
| Parallel 10–15 (Claude) | Best practical | Same tokens | Manageable 429s |
| Very high concurrency (50+) | Marginally faster | Same tokens | More failures, messier logs |
| Anthropic Batch | Slower than live parallel | Often lower $ | Weaker interactive debug |

**Recommendation:** Live parallel with checkpointing for Phase 1; provider-isolated parallel for Phase 2. Use Batch only if cost pressure is high and timeline is flexible.

---

## Cursor Feedback: Report Design

### Overall verdict
The proposed structure is strong for investor/NDA use: methodology in-body (not appendix), full 159 transparency, sidecar raw data, self-contained methods footer. **Keep this skeleton.**

### Suggested improvements

1. **Define the ranking metric in Section 1 and Section 3 explicitly**  
   Add a one-box “Scoring Rule” early:
   - Compression ratio definition (vs English baseline tokens)
   - Fidelity = count of passed methods / 5
   - Eligibility for Phase 2 (e.g., compression ≤ 1.0 **and** fidelity ≥ 3/5 **and** consistent across levels 1–3)
   - Exact sort keys for “top 20–30”

2. **Clarify “fidelity level” vs “fidelity method”**  
   Investors will confuse these. Add a terminology callout:
   - **Levels 1–3** = representation intensity / encoding variants tested
   - **Methods 1–5** = independent checks that produce the k/5 score

3. **Results table — recommended columns**
   | Script | ISO/Unicode ID | Level 1 Comp | L1 Fid (x/5) | Level 2 Comp | L2 Fid | Level 3 Comp | L3 Fid | Composite Rank Score | Phase-2 Eligible? | Notes |
   Keep a second view: **failures gallery** (zero fidelity / expansion) so transparency is visible without forcing investors to scan 159 rows.

4. **Distribution visualization**  
   Add 2–3 charts (not a dashboard dump):
   - Histogram of fidelity scores (0–5)
   - Scatter: compression vs fidelity
   - Stacked counts: compress+pass / compress+fail / expand / zero

5. **Sidecar raw data contract**  
   Specify machine-readable schema up front (JSONL or CSV):  
   `script_id, script_name, level, provider, model_id, timestamp, input_tokens, output_tokens, compression_ratio, method_1..method_5, methods_passed, raw_outputs_path`  
   One row per script×level (Phase 1) / script×level×provider (Phase 2).

6. **Methodology footer — add reproducibility block**
   - Exact model IDs and API versions/dates
   - Temperature / decoding params
   - English baseline token count
   - Random seeds if any
   - Exclusion rules (context overflow, API errors)

7. **Column structure note**  
   For the main PDF/report, prefer **ranked top 30 full detail + summary stats for all 159**, with complete 159 table in sidecar + HTML/CSV. A 159-row dense table in the narrative PDF hurts readability; transparency is preserved if the sidecar is first-class and linked.

8. **Investor one-pager front**  
   Optional half-page before Exec Summary: claim → evidence → limitation. Helps VC skimmers without weakening the full audit trail.

### What not to change
- No cherry-picking
- Methods explained in the main report body
- Failures included
- Self-contained methodology section

---

## Constraints & Scope Adjustments (Recommendations)

| Adjustment | Why |
|---|---|
| **Unblock Q1 before any run** | Investor methodology section is blocked without Methods 1–5 |
| **Confirm call graph of each method** | Swings Phase 1 cost from ~$25 to ~$300 |
| **Cap expansion** | Hard-fail iterations that exceed N× baseline tokens |
| **Phase 1 = Claude only, full 159** | Keep as designed (good Zipfian / transparency story) |
| **Phase 2 = only locked top list** | Prevents budget creep |
| **Drop providers lacking keys/token APIs** | Better than approximate silent substitutes |
| **Run harness outside `lifebutwrong`** | Wrong repo for this workstream |
| **Optional cost saver** | Local/heuristic methods on all 159; LLM-judged methods only if compression passes |

### Scope cut options (if budget-constrained)
1. **159 scripts × compression-only screen**, then full 5-method fidelity on top 40, then Phase 2 on top 20  
2. **Phase 2 with 4 providers first** (Anthropic, OpenAI, Google, Grok), expand later  
3. **Single fidelity level for Phase 1 screen**, re-test levels 1–3 only on top 30  

I do **not** recommend cutting the “show the failures” requirement; that is core to the investor narrative.

---

## Direct Answers Checklist

| Item | Status |
|---|---|
| Q1 Methods 1–5 definitions | **Blocked** — need Tests 1–3 source |
| Q2 Effort / cost / parallel feasible? | **Answered** — parallel yes; budget bands above |
| Q3 Parallelization strategy | **Answered** — recommended plan above |
| Report design feedback | **Answered** — keep structure + scoring/term/sidecar upgrades |
| Resource feasibility | **Feasible** at Mid band with concurrency; confirm method call counts |
| Test 4 executed? | **No** |

---

## Next Steps (aligned to brief)

1. ~~Cursor answers Q1–Q3~~ → Q2/Q3 done; **Q1 awaiting materials**
2. Phil & team review this response; send Tests 1–3 fidelity-method definitions
3. Cursor revises Q1 with exact auditable algorithms
4. Adjust scope/budget if needed
5. **Phil explicit approval** to execute Test 4
6. Only then: build/run Phase 1 → report + sidecar → Phase 2 planning

---

## Ask of Phil / team

Please send the Tests 1–3 fidelity methodology (paste is fine from phone). Minimum needed:

1. Name + one-sentence purpose of Methods 1–5  
2. Pass/fail rule for each  
3. Whether each method is local code or requires an LLM judge call  
4. How Levels 1–3 differ  

With that, Q1 can be completed to investor standard without guessing.
