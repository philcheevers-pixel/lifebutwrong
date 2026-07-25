# TRACE ON — Single Record Walkthrough
**Document:** CB-Cursor-TRACE-ON-Single-Record-20260725  
**Date:** July 25, 2026  
**Status:** Explanation only — **no live Test 4 run**  
**Audience:** Phil (before we institute the full program)

---

## Did your prompt make sense?

Yes. You asked for the old DOS/batch equivalent of:

```
TRACE I   ← turn step-by-step logging ON
RUN once  ← one record only
TRACE O   ← turn it OFF
```

You are **not** asking for the full 159-script Test 4 yet.  
You want to see **exactly** what happens between:

1. Sending the original message out  
2. Getting the model response back  
3. Analyzing / measuring both sides  

That is the right question. Below is that trace, explained first. We do **not** fire a live LLM call until you say so.

---

## What “one record” means here

One record = **one representation** of the same essay, put through the full measurement pipeline.

| Piece | Value (from Runs 01–03) |
|---|---|
| Essay | *“Why You Should Treat Your AI Well”* |
| English size (tokens) | **1,661** (Claude Sonnet 4.6) |
| English size (words) | Your “**1,476 words**” figure is plausible as a **word count**; the lab docs measure **tokens**, not words. Tokens ≈ words ÷ ~0.75, so ~1,476 words ≈ ~1,660–2,000 tokens depending on tokenizer. We treat **1,661 tokens** as the official English baseline. |
| Example record used below | **Code Notation** (best-documented compressor from Run 01/03) |

Other records would be Chinese, Oriya, Swahili, Egyptian, etc. Same steps; different numbers.

---

## TRACE I — Turn the lights on

What follows is every step for **one record**, with the measurements that go **out** and come **back**.

---

### STEP 0 — Load the original English payload

```
OUTBOUND (human → harness)
  payload_id:     essay_treat_ai_well
  language:       English
  words:          ~1,476   (your figure; not used as the ranking key)
  tokens_en:      1,661    (official baseline T_en)
  provider:       Anthropic
  model:          claude-sonnet-4.6
```

Nothing has been sent to the model yet. We only establish the yardstick.

---

### STEP 1 — Build the representation R (encode)

```
LOCAL TRANSFORM (no LLM yet, or offline encoder)
  input:   English essay
  method:  Code Notation encoder   ← this is "the record"
  output:  R   (the encoded string)

MEASURE
  tokens_r = tokenize(R)
  Example (Run 01 Code Notation):
    tokens_r = 548
```

**Measurement that leaves this step:**

| Field | Formula / value |
|---|---|
| `T_en` | 1,661 |
| `T_r` | 548 |
| `compression_pct` | `(1661 − 548) / 1661 × 100` = **67.0%** reduction |
| `expansion?` | no (`T_r < T_en`) |

If `T_r > T_en`, this record is an **expander** (e.g. Oriya +424%). Scientifically interesting; not a Raquel cost win.

---

### STEP 2 — Level 1A Echo (send → respond → compare)

This is the first real round-trip to the model.

```
OUTBOUND (harness → model)
  instruction:  "Echo / repeat the following text exactly."
  body:         R   (the encoded payload, 548 tokens)
  tokens_in:    ~548 + instruction overhead

INBOUND (model → harness)
  output O:     model's attempt to repeat R
  tokens_out:   length of O in tokens

ANALYZE
  echo_pct = similarity(O, R)   # character-level or documented %
  Example (Run 03 Code Notation): echo_pct = 100%
```

**What this proves:** the model can *see* the glyphs/data.  
**What this does not prove:** that it understood the essay.

| Measurement out | Measurement back |
|---|---|
| encoded payload R | echoed string O |
| tokens_in | tokens_out |
| — | echo_pct (e.g. 100%) |

---

### STEP 3 — Level 1B Round-trip / meaning check

Second model call. Same payload, different ask.

```
OUTBOUND (harness → model)
  instruction:  "Using the text below, restore / answer about the ORIGINAL meaning."
  body:         R
  tokens_in:    ~548 + instruction overhead

INBOUND (model → harness)
  output:       reconstruction or answers about meaning
  tokens_out:   length of response

ANALYZE
  roundtrip_result = PASS or FAIL
  against original English meaning

Example (Run 03 Code Notation): FAIL
  Reason: Claude paraphrases; it does not replay text word-for-word.
  This is expected LLM behavior — not proof Raquel is useless.
```

**Recommendation already on the table:** treat Level 1B as **diagnostic**, not a hard kill switch. Ranking leans on Level 2 + compression.

| Measurement out | Measurement back |
|---|---|
| encoded payload R + meaning ask | semantic response |
| tokens_in | tokens_out |
| — | roundtrip_result (PASS/FAIL + notes) |

---

### STEP 4 — Level 2 Theme / Scotty audit (the “3 out of 5”)

Third model call. This is the idea-level test investors care about.

```
OUTBOUND (harness → model)
  instruction:  "List the five main themes / answer these five fixed questions."
  body:         R
  tokens_in:    ~548 + instruction overhead

INBOUND (model → harness)
  output:       themes or answers
  tokens_out:   length of response

ANALYZE
  themes_k = how many of the 5 reference items were recovered
  themes_of = 5
  score     = k/5

English baseline (Run 02/03):  3/5
Code Notation (Run 03 themes): 4/5   ← better than English
```

**“3 out of 5” is not five different methods.**  
It is the score on a **five-item checklist** for this one record.

| Measurement out | Measurement back |
|---|---|
| encoded payload R + theme/question ask | theme list / answers |
| tokens_in | tokens_out |
| — | themes_k / 5 (e.g. 4/5) |

---

### STEP 5 — Roll up the record card

After Steps 1–4, one record produces one summary row:

```
RECORD CARD — Code Notation (example from Runs 01–03)
────────────────────────────────────────────────────
script_name:        Code Notation
tokens_en:          1661
tokens_r:           548
compression_pct:    67.0%
level_1a_echo_pct:  100%
level_1b_roundtrip: FAIL (paraphrase — diagnostic)
level_2_themes:     4/5
phase2_eligible?:   YES
                    because (tokens_r < 1661) AND (themes >= 3)
────────────────────────────────────────────────────
```

That is the entire transformation for **one** record:

```
English essay
    → encode to R
    → measure size (compression)
    → send R for Echo      → measure echo_pct
    → send R for Meaning   → measure PASS/FAIL
    → send R for Themes    → measure k/5
    → write one record card
```

---

## TRACE O — Lights off

Stop after one record. Do **not** loop 159 scripts.  
Do **not** start Phase 2.  
Do **not** write the investor PDF yet.

---

## Side-by-side: what goes out vs what comes back

| Stage | Goes OUT | Comes BACK | Stored measurement |
|---|---|---|---|
| 0 Baseline | English essay (local) | — | `tokens_en = 1661` |
| 1 Encode | English → encoder | R | `tokens_r`, `compression_pct` |
| 2 Level 1A | R + “echo exactly” | O | `echo_pct`, `tokens_in/out` |
| 3 Level 1B | R + “original meaning?” | semantic reply | `roundtrip_result`, `tokens_in/out` |
| 4 Level 2 | R + “5 themes/questions” | answers | `themes_k/5`, `tokens_in/out` |
| 5 Rollup | record card fields | — | `phase2_eligible` |

Approx. **3 LLM calls** per record (1A + 1B + 2), plus local tokenization.

---

## How this relates to the full Test 4 program

| Mode | What runs |
|---|---|
| **TRACE ON / one record** (this doc) | One representation, every step visible |
| **Test 4 Phase 1** (not approved yet) | Same pipeline × **159** Unicode scripts |
| **Test 4 Phase 2** (later) | Top 20–30 × 3 levels × 8 providers |

Your instinct is right: understand **one** fully traced record before you turn the batch job loose.

---

## What I still need from you before a live TRACE run

I can explain forever from the July 22 numbers. A **live** single-record TRACE needs:

1. **Which record?** English baseline, Code Notation, or another script?  
2. **Essay text** available in this environment (or pasted). The lab docs name it; the text itself is not in `lifebutwrong` or `tokenscope`.  
3. **Explicit go-ahead** for one live LLM call set (3 calls). Prior brief still said **DO NOT RUN TEST 4** until approval — a one-record TRACE is smaller, but I will not fire it without your OK.  
4. Confirm the open scoring rules from the Test 4 response:
   - 3 levels + Scotty k/5 (not “5 methods”)?
   - Phase-2 gate = compress **and** Level 2 ≥ 3/5?
   - Level 1B diagnostic only?
   - Abort if `tokens_r` > 3× or 5× English?

---

## Bottom line

Your prompt was not malformed. You want **TRACE I → one record → TRACE O**, with every outbound payload and inbound measurement shown.

Above is that walkthrough using the real Code Notation numbers from Runs 01–03.  
**No live job was run.** Say the word when you want the live one-record TRACE executed, and which representation to use.
