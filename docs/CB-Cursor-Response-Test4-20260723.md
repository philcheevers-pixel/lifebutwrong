# Cursor Response: Test 4 Brief (CB-Cursor-Brief-Test4-20260724)
**Version:** 2 (Q1 unblocked)  
**Date:** July 23, 2026  
**Status:** Prerequisite answers complete — awaiting Phil & team review  
**CRITICAL:** Test 4 was **NOT** executed. Awaiting explicit approval before any run.

**Sources used:**
1. `CB-Cursor-Brief-Test4-20260724` (design brief)
2. `TS-Raquel-Testing-Documentation-Complete-20260722` (Tests / Runs 01–03 reference)

---

## Receipt Confirmation

Both documents received. Scope unchanged:
- Phase 1: 159 Unicode scripts × 3 fidelity levels on Claude Sonnet 4.6 (477 iterations)
- Phase 2: Top 20–30 × 3 levels × 8 providers (≈480–720 iterations)
- **No test execution until explicit approval**

---

## Important Terminology Correction (Read First)

The Test 4 brief asked for **“five fidelity methods”** and how **“3 out of 5”** works. The July 22 testing documentation shows something different and more precise:

| Phrase in Test 4 brief | What Tests 1–3 actually mean |
|---|---|
| “Five fidelity methods” | **Not five separate methods.** There are **three fidelity checks** (Level 1A, Level 1B, Level 2). |
| “3 out of 5” | Score on the **Scotty five-question / five-theme audit**: how many of five questions (Run 02) or five key themes (Run 03 Level 2) the model got right. English baseline was **3/5**. |
| “3 fidelity levels” | Maps cleanly to Run 03: **Level 1A (Echo)**, **Level 1B (Round-trip)**, **Level 2 (Theme audit)**. |

**Recommendation for investor report wording:** Do **not** say “five fidelity methods.” Say:
1. **Three fidelity levels** (Echo / Round-trip / Theme), and
2. Within Level 2 (and Run 02’s Scotty v1), a **five-item checklist** scored as **k/5**.

If Phil intended five distinct methods beyond what Run 01–03 document, that needs to be stated explicitly — it is not in the July 22 reference.

---

## Question 1: Fidelity Methods / Levels (CRITICAL) — ANSWERED

Based on `TS-Raquel-Testing-Documentation-Complete-20260722`.

### What Raquel is testing (one sentence)
Raquel asks whether a non-English representation of the same essay can **shrink inbound tokens** while still letting the model **preserve meaning** well enough for useful work.

### English baseline (from Run 01)
- Payload: essay *“Why You Should Treat Your AI Well”*
- English: **1,661 tokens** (Claude Sonnet 4.6)
- Compression % = how much smaller inbound became vs this baseline

---

### Check A — Compression measurement (Run 01; not a fidelity check)
**What it tests:** Token size only. Does the representation shrink inbound data?  
**Algorithm:**
1. Tokenize English essay → `T_en` (baseline = 1,661).
2. Produce representation R (Code Notation, Chinese, Oriya, etc.).
3. Tokenize R → `T_r`.
4. Compression reduction % = `(T_en − T_r) / T_en × 100`.
5. Expansion if `T_r > T_en`.

**Success / failure (operational):**
- **Success (compresses):** `T_r < T_en` (target band cited: 25–35% reduction; Code Notation hit 67%).
- **Neutral / fail for Zipfian ranking:** no reduction or expansion (Chinese ≈0%; Swahili +69%; Oriya +424%).

**Why it matters:** Without compression, Raquel has no cost thesis. Fidelity alone is not enough.

---

### Method / Level 1A — Echo Fidelity (Run 03)
**What it tests:** Character-level (or near-exact) reproduction. Did the model echo back what it received?  
**Investor plain language:** “Can the AI repeat the encoded text accurately?”

**Algorithm:**
1. Send encoded payload to the model with an echo / repeat instruction.
2. Receive output string `O`.
3. Compare `O` to the encoded input `R` (character-by-character or documented similarity %).
4. Record exact-match % (or 0% if unparseable).

**Pass / fail (as used in Run 03):**
- **Pass / strong:** ~100% exact match (English, Code Notation, Swahili).
- **Soft pass / note:** high but imperfect (Oriya 96.97%).
- **Fail:** 0% / cannot read (Egyptian Hieroglyphics, Cuneiform).

**Failure looks like:** Model cannot parse the script, returns refusal/garbage, or diverges materially from the input string.

**Why it matters:** Confirms the representation is at least legible to the model as data. Does **not** prove meaning was understood.

---

### Method / Level 1B — Round-Trip / Semantic Fidelity (Run 03)
**What it tests:** Semantic preservation under reconstruction. When asked about the original meaning (or to restore meaning), does the model demonstrate correct understanding?  
**Investor plain language:** “If we ask about the ideas in the encoded text, does the AI get the original meaning right?”

**Algorithm (as described):**
1. Send encoded payload.
2. Ask the model questions about / reconstruction of the **original meaning**.
3. Score whether the response preserves the original semantics (documented as PASS/FAIL in Run 03).

**Pass / fail (Run 03 results):**
- English baseline: **PASS**
- Code Notation, Oriya, Swahili, Egyptian, Cuneiform: **FAIL** under a strict “reproduce original” reading

**CRITICAL FINDING (carry into Test 4 report verbatim in spirit):**  
Claude tends to **paraphrase**, not replay text word-for-word. Encoded versions failed Level 1B when judged as exact reconstruction. That is expected LLM behavior, not proof Raquel is useless.  
**Patent / investor implication from Run 03:** Do **not** claim lossless character-level compression. **Do** claim **idea-level preservation** (Level 2).

**Why it matters:** Separates “can echo glyphs” from “understood the essay.” Also prevents overclaiming.

---

### Method / Level 2 — Theme Audit / Scotty (Run 02 v1 questions + Run 03 themes)
**What it tests:** Idea-level fidelity. Can the model identify the same key ideas from the encoded text as from English?  
**Investor plain language:** “Does the AI still see the main points?”

**Two related scorings in the July 22 docs:**

#### Run 02 — Scotty v1 five-question audit
1. Encode essay into representation R.
2. Ask **5 fixed questions** about the content.
3. Score **k/5** correct answers.
4. Compare to English baseline (**3/5** in Run 02).

**Examples from Run 02:** Code Notation 3/5; Oriya 4/5; Swahili 5/5; Egyptian/Cuneiform unparseable.

#### Run 03 — Level 2 five-theme audit
1. Establish English reference themes (model listed **3 of 5** key themes on English).
2. Ask model to list the **five main themes** from encoded version.
3. Score how many of the five reference themes were recovered (**k/5**).

**Examples from Run 03 Level 2:** Code Notation **4/5** (better than English); Oriya 4/5; Swahili 3/5; Egyptian/Cuneiform 0/5.

**Pass / fail (recommended for Test 4 ranking — confirm with Phil):**
- **Production-candidate floor:** ≥ English baseline on Level 2 (i.e., ≥3/5 themes), **and** compression (`T_r < T_en`).
- **Strong:** ≥4/5 themes with compression (Code Notation profile).
- **Fail:** 0/5 or unparseable; or high themes **with expansion** (interesting scientifically, not a Raquel win).

**Why it matters:** This is the Run 03–endorsed measurement standard for claims: **idea-level preservation**.

---

### How to explain “3 out of 5” in the Test 4 investor report

> **“3 out of 5” is not a count of five different test methods.**  
> It is the score on a **five-item content checklist** (five questions in Run 02, or five themes in Run 03 Level 2).  
> The English baseline scored **3/5**. A result of **3/5** means the model recovered three of the five expected items — matching baseline. **4/5** or **5/5** means stronger idea recovery than the English run. **0/5** usually means the model could not read the representation.

If the report needs a single fidelity headline per script, recommend:
- Report **Level 1A %**, **Level 1B PASS/FAIL** (with paraphrase caveat), and **Level 2 k/5**
- Use **Level 2 k/5 + compression** as the primary Zipfian sort key

---

### Mapping to Test 4’s “159 × 3 fidelity levels”
Treat each script’s three iterations as:
1. Level 1A Echo  
2. Level 1B Round-trip  
3. Level 2 Theme audit (Scotty)

That yields 159 × 3 = 477 documented check results, matching the brief’s Phase 1 arithmetic.

---

## Question 2: Level of Effort & Resource Constraints (UPDATED)

Baseline confirmed: **1,661 English tokens**.

### Call model (refined)
Per script, Phase 1 likely needs roughly:
- 1× tokenization / size measurement (local or tokenizer API)
- 1× Level 1A echo call
- 1× Level 1B round-trip call
- 1× Level 2 theme-list call  
≈ **3 LLM calls per script** for the three fidelity levels, plus optional English reference once globally.

For 159 scripts: ≈ **480 LLM calls** (± retries), not 477×5.

| Phase | Wall-clock (parallel 10–15) | Est. API cost (Sonnet 4.6) | Notes |
|---|---|---|---|
| **Phase 1** | **2–6 hours** | **~$25–90** | Mid band; encoded scripts that expand (Oriya-class) cost more |
| **Phase 2** (20–30 × 3 × 8) | **1–3 days** | **~$80–350** | Dominated by provider limits/keys |

### Constraints to flag
1. **OpenAI token-counting API** — if unavailable, exclude or use documented tiktoken fallback and label it.
2. **Expansion bombs** — Oriya-class +424% will dominate cost/context; set abort if `T_r > N × 1,661` (recommend N=3 or 5).
3. **Level 1B scoring rule** — must be decided pre-run: exact reconstruction will fail broadly (Run 03). Prefer graded semantic rubric or treat 1B as diagnostic, Level 2 as ranking.
4. **Provider auth matrix** for Phase 2 (8 providers).
5. **Perplexity/OpenRouter** — record underlying model IDs.
6. Execute in a Raquel/test harness repo, not `lifebutwrong`.

---

## Question 3: Parallelization & Batching Strategy

**Unchanged recommendation; refined to 3 calls/script:**

### Phase 1
1. Precompute encodings locally where possible.
2. Worker pool concurrency **10–15** on Claude.
3. Per script: measure tokens → 1A → 1B → 2; write JSONL checkpoint after each level.
4. Global English baseline themes/questions run **once**, reused for all Level 2 comparisons.
5. Retry 429/5xx with exponential backoff; do not lose partial script results.

### Phase 2
1. Freeze top 20–30 from Phase 1 ranking.
2. Parallelize within each provider (concurrency ~3–8).
3. Reuse the same encoded payloads across providers.

**Trade-off:** Parallelism cuts wall-clock; token spend stays ~constant. Anthropic Batch can cut $ ~50% if async delay is acceptable.

---

## Report Design Feedback (UPDATED)

### Keep
- Exec summary, in-body methodology, all 159 results (including failures), sidecar raw data, self-contained methods section, investor/NDA tone.

### Must-fix from July 22 learnings
1. **Replace “five fidelity methods”** with **three levels + five-item Scotty score**.
2. **Scoring box up front:**
   - Compression vs 1,661-token English baseline
   - Level 1A echo %
   - Level 1B semantic result (with paraphrase caveat)
   - Level 2 theme score k/5
   - Phase-2 eligible iff compresses **and** Level 2 ≥ 3/5 (confirm threshold)
3. **Patent caution callout:** idea-level preservation (Level 2), not lossless character-level (Level 1B).
4. **Ranked top 30 in PDF** + full 159 in sidecar/CSV.
5. **Charts:** compression vs Level 2 score; histogram of k/5; failure classes (expand / unparseable / compress+pass).

### Recommended ranking metric (propose)
```
eligible = (tokens_r < 1661) AND (level2_themes >= 3)
sort = (-level2_themes, tokens_r ascending, -level1a_pct, script_name)
top 20–30 = first eligible rows; if <20 eligible, take best compressors with notes
```

### Sidecar columns
`script_id, script_name, level, provider, model_id, timestamp, tokens_in, tokens_out, tokens_vs_english, compression_pct, echo_pct, roundtrip_result, themes_k, themes_of, phase2_eligible, notes, raw_path`

---

## Constraints & Adjustments

| Item | Recommendation |
|---|---|
| Brief’s “5 methods” language | Correct to 3 levels + Scotty k/5 before investor draft |
| Level 1B as hard gate | **No** — use as diagnostic; Level 2 + compression for ranking |
| Ancient / untrained scripts | Expect 0% echo, 0/5 themes; keep in dataset for transparency |
| Expansion languages (Swahili/Oriya class) | Document high fidelity if present; exclude from “Raquel win” set |
| Scope cut if needed | Full 159 compression+1A cheap screen, full 1B/2 on compressors only |

---

## Direct Answers Checklist

| Item | Status |
|---|---|
| Q1 fidelity definitions | **Answered** from July 22 doc (3 levels; “3/5” = Scotty score) |
| Q2 effort / cost | **Answered** — Phase 1 ~$25–90 / 2–6h parallel |
| Q3 parallelization | **Answered** — concurrency 10–15 + checkpoints |
| Report design | **Answered** — keep structure; fix terminology + scoring box |
| Test 4 executed? | **No** |

---

## Next Steps

1. Phil & team confirm: (a) terminology correction accepted, (b) Level 2 ≥3/5 + compression as Phase-2 gate, (c) Level 1B diagnostic not hard fail.
2. Adjust scope/budget if desired.
3. **Explicit approval** to execute Test 4 Phase 1.
4. Only then: build harness → run 159 scripts × Levels 1A/1B/2 on Claude → investor report + sidecar.

---

## Open Confirmations Needed From Phil

1. Accept renaming “five methods” → **three fidelity levels + Scotty five-item score**?
2. Confirm Phase-2 eligibility: **compression AND Level 2 ≥ 3/5**?
3. Confirm Level 1B is **diagnostic** (paraphrase expected) rather than a hard pass gate?
4. Abort threshold for token expansion (suggest **3×** or **5×** English = 4,983 / 8,305 tokens)?
