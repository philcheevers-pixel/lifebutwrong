# Raquel / Pinkhouse — Trial Installation Playbook

**Audience:** Phil (founder) + customer technical contact  
**Moment:** Customer says **yes to a test** (or yes to buy — still start with a controlled trial)  
**Brand:** TokenScope / Raquel / Pinkhouse only — not Life But Wrong  
**Default path:** SaaS on your cloud (e.g. DigitalOcean) — customer calls *out* to you  
**Length:** ~3–4 pages working procedure  

---

## 0. Why the trial comes first

A “buy” without a measured trial is how deals die in procurement.  
A **test** is the make-or-break moment: same job, fewer tokens, readable receipt.

**Rule:** Even if they say “we want to buy,” run **Trial → Proof → Expand → Contract.**

---

## 1. What “trial installed” means (definition of done)

The trial is **done** when all of the following are true:

1. Customer staging (or a thin slice of traffic) reaches **your Raquel plug** instead of calling Anthropic directly.  
2. For each trial call (or batch), you both can see:
   - tokens **before** shrink  
   - tokens **after** shrink  
   - fidelity / success check (pass/fail or score)  
   - timestamp + trial id  
3. At least **N successful jobs** complete end-to-end (suggest **20–50** staging calls, or one agreed real workload).  
4. A one-page **Trial Receipt** is shared (PDF or TokenScope export).  
5. Customer can rip you out in one config change (fail-safe / off switch).

If you only “sent software” and nobody saw before/after counts, the trial is **not** installed.

---

## 2. Roles (who does what)

| Role | Person | Job in the trial |
|---|---|---|
| Sponsor | Their VP IT / FinOps / product owner | Approves test; cares about $ |
| Tech lead | Their engineer | Points staging at your API; runs sample jobs |
| Security watcher | Their sec/ops (often) | Watches; allowlists; keys |
| Phil | You | Tenant, keys, docs, joint call, meter, receipt |
| Build support | You + Cursor (later hire) | Keep the plug up; fix trial bugs fast |

**Phil does not:** sit on-site, install chips, touch their production unattended on day one.

---

## 3. Pre-flight (before the install call) — Phil checklist

Do these the same day they say “we’ll test,” if possible:

- [ ] Create **tenant**: `customer-slug` on Pinkhouse / TokenScope  
- [ ] Create **trial API key** (scoped, expiring — e.g. 14 or 30 days)  
- [ ] Confirm plug is up: health URL green  
- [ ] Confirm **fail-open** behavior documented (if plug errors → option to bypass or clear error)  
- [ ] Prepare **canned sample** (known token counts) *and* invite **their sample**  
- [ ] Send **Trial Pack** email (template below)  
- [ ] Book **Install Call** (45–60 min) + optional **Readout Call** (20 min) 3–7 days later  
- [ ] Agree in writing: **staging only** until readout  

### Trial Pack email (send immediately)

Subject: `Pinkhouse / Raquel trial — setup pack`

> Thanks for agreeing to test.  
>  
> **What we’re proving:** same job → fewer tokens to Anthropic → you can see before/after counts.  
> **Where it runs:** our cloud plug (you call us; we forward to Anthropic). No on-site install.  
>  
> **Your items:**  
> 1. Trial API base URL: `https://api.pinkhouse.com/...` *(or current URL)*  
> 2. Trial API key: *(separate secure channel if needed)*  
> 3. Setup sheet: change Anthropic base URL / client to our endpoint; send key in header `Authorization: Bearer …`  
> 4. Staging only for this trial.  
>  
> **Install call:** *(date/time)* — your engineer + me. We’ll run canned + your sample and watch the meter.  
> **Success:** exportable Trial Receipt with before/after tokens.  
>  
> If anything looks wrong, flip back to direct Anthropic in one config change.

---

## 4. Commercial frame for the trial (keep light)

Agree **before** traffic:

| Item | Suggested default |
|---|---|
| Duration | 14 days (or 30) |
| Environment | Staging / non-prod first |
| Volume cap | e.g. max N requests/day or max $ of underlying model spend |
| Price for trial | $0 or small setup fee (your choice) |
| Data | Their samples stay theirs; you log meters, not their secrets, per agreement |
| Success metric | Median crush % on agreed job types + fidelity gate passed |
| Next step if success | Paid pilot or contract discussion using **same meter formula** |

Do **not** argue 5%-of-savings invoice math on hour one of trial. Prove the meter first.

---

## 5. Technical install steps (Path A — SaaS)

### 5.1 Mental picture
```
[Rogers app / staging]
        |  HTTPS API call + your trial key
        v
[Raquel plug on DigitalOcean / Pinkhouse]
  1. count tokens BEFORE
  2. Rosetta / shrink
  3. count tokens AFTER
  4. log to TokenScope
        |
        v
[Anthropic]
        |
        v
[Raquel plug]  (return / decode as needed)
        |
        v
[Rogers app]
```

Rosetta lives on **your plug**, not inside Anthropic.

### 5.2 Customer engineer steps (they do this)
1. In **staging**, locate where the Anthropic (or multi-model) client is configured.  
2. Set API base URL to Pinkhouse trial URL **or** insert “Raquel client” per your doc.  
3. Set trial API key.  
4. Keep Anthropic key available as required by the chosen pattern:
   - **Pattern A (common early):** customer stores Anthropic key with you for the trial (strict controls), **or**  
   - **Pattern B (often preferred later):** customer keeps Anthropic key; your plug shrinks and returns crushed payload for *them* to send — harder for “full middle”; for full middle gateway, Pattern A or a vaulted key is typical.  
   *Decide one pattern before the call and document it.* For a true middle plug that calls Anthropic for them, they must trust you with key access or use a temporary project key.  
5. Run health check / “hello” request.  
6. Do **not** point production until readout.

### 5.3 Phil steps on the install call (minute-by-minute)

**0:00–0:05** — Frame  
“Staging only. One job path. We want a receipt, not a tour.”

**0:05–0:15** — Connectivity  
- Health check  
- Auth works  
- First canned sample through  

**0:15–0:35** — Proof runs  
- Canned sample: record before/after/fidelity  
- Their sample: same  
- One failure test: bad key / empty body — show clear error, no mystery hang  

**0:35–0:50** — Meter walkthrough  
- Open TokenScope (or shared dashboard)  
- Show how to filter by trial id  
- Export or screenshot Trial Receipt draft  

**0:50–0:60** — Off switch + homework  
- How to disable (revert base URL)  
- Agree volume for next 3–7 days  
- Book readout  

### 5.4 DNS vs API (one more time)
- They call your **DNS name** (host).  
- They speak your **API** (paths, headers, JSON).  
- You do not need their corporate DNS.  
- They do not need your stapler.

---

## 6. During the trial window (days 1–14)

**Customer**
- Runs agreed staging workloads  
- Notes anything broken (timeouts, quality)  
- Does not expand to prod without readout  

**Phil (daily light touch)**
- Check error rate / uptime  
- Spot-check crush % and fidelity  
- Reply same day to blockers (make-or-break)  
- Do **not** change secret sauce mid-trial without telling them  

**Red flags (act immediately)**
- Fidelity failures above agreed gate  
- Timeouts / their staging blocked  
- Meter missing before/after (can’t prove savings)  

---

## 7. Trial Receipt (what you hand them)

One page. No novel.

| Field | Example |
|---|---|
| Customer / trial id | Rogers-staging-2026-08-01 |
| Period | dates |
| Jobs measured | 42 |
| Median tokens before | 1,661 |
| Median tokens after | 548 |
| Median crush % | 67% |
| Fidelity gate | Echo / Scotty rule you agreed — pass rate |
| Underlying model | Claude … |
| Notes | languages / job types included |
| Off switch tested | yes/no |

Line for humans:

> “Same measurement you can use at scale. This trial is a clean sample / staging slice. Volume comes after.”

---

## 8. Readout call (make-or-break conversation)

**Agenda (20–30 min)**
1. Show Trial Receipt.  
2. Ask: “Does this match the job types you care about?”  
3. If yes → propose **paid pilot** (more volume, still capped) or **contract**.  
4. If mixed → narrow job types; extend trial 7 days.  
5. If no → thank them; leave off switch; learn.  

**If moving toward buy / % of savings**  
Only now lock the formula:

`Saved_tokens = T_before − T_after`  
`Saved_$ = Saved_tokens × agreed rate (or attributed Anthropic invoice)`  
`Fee = % × Saved_$` (plus optional minimum)

Without before/after from **your meter**, do not sell %-of-savings.

---

## 9. If they said “buy” instead of “test”

Same install. Faster paperwork. Still:

1. Trial/pilot on staging  
2. Receipt  
3. Expand  
4. Invoice terms  

Never skip the meter.

---

## 10. Phil’s personal level of effort (honest)

| Phase | Your time (order of magnitude) |
|---|---|
| Trial Pack + tenant/key | 30–90 minutes |
| Install call | 45–60 minutes |
| Babysit 1–2 weeks | 15–30 minutes/day unless fire |
| Readout + next proposal | 30–60 minutes |
| On-site hardware | **None** |

Build/fix of the plug itself is product work **before** many trials — once — on DigitalOcean. Each new customer reuses it with a new key.

---

## 11. One-page sticky checklist (print this)

**When they say yes to test**
1. Tenant + expiring trial key  
2. Trial Pack email  
3. Book install call + readout  
4. Staging only  
5. Canned + their sample through plug  
6. Before / after / fidelity visible  
7. Off switch confirmed  
8. Trial Receipt  
9. Readout → pilot or stop  

**Remember**
- Plug in the middle; Rosetta on your server  
- They API out to you  
- No chips, no desk PC, no Life But Wrong  
- Make-or-break = receipt, not speech  

---

## 12. Open items to decide once (company standards)

Fill these in when your head is clear; don’t invent per customer:

1. Trial length default: ___ days  
2. Key custody pattern (A vaulted Anthropic key vs B other): ___  
3. Fidelity gate for “pass”: ___  
4. Volume / $ cap: ___  
5. Trial fee: $0 / $___  
6. Exact API paths and header names: ___  
7. Fail-open vs fail-closed default: ___  

---

*End of trial installation playbook. Pair with `TokenScope-Raquel-Demo-Sales-Coaching.md` for outreach and 5-minute demo; this document starts at “yes, we’ll test.”*
