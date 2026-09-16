# CarveIntel

Pharmaceutical patent intelligence — ABFTO reports.

## Identity

- **Live URLs:** https://carveintel.com/ · mirror https://pinkhouse.tech/carveintel/
- **Source path:** `sites/carveintel/` in `philcheevers-pixel/lifebutwrong` (bootstrap)
- **Status:** `git-backed-bootstrap` — recovered from live on 2026-09-16; confirm against laptop copy

## Page flow (3 screens)

| # | File | Role |
|---|---|---|
| 1 | `index.html` | Front page — ABFTO pitch + Start Your Order |
| 2 | `intake.html` | Inventor intake — claims, molecule, files, notes (16 questions / 6 domains) |
| 3 | `report.html` | ABFTO Intelligence Report viewer (cover, sidebar TOC, print/PDF, 6 languages) |

Supporting demos:

| File | Role |
|---|---|
| `walkthrough.html` | Friday walkthrough entry — opens demo reports without live API |
| `jobs/aspirin_demo_report.json` | Complete ABFTO demo (10 sections) — `report.html?token=DEMO_ASPIRIN` |
| `jobs/lm-299_demo_report.json` | Template-in-progress ABFTO (11 sections) — `report.html?token=DEMO_LM299` |
| `jobs/intake_lm-299.json` | Sample intake payload for LM-299 |

## Hosting

- **DNS:** Cloudflare (`indie` / `josh` NS)
- **Origin:** Apache on Pink House droplet (same bytes as `/carveintel/`)
- **Deploy path:** `/var/www/html/carveintel/`

## Deploy

```bash
# from machine with SSH to the droplet
rsync -av --delete ./sites/carveintel/ USER@pinkhouse.tech:/var/www/html/carveintel/
# if carveintel.com shows stale HTML, purge Cloudflare cache for the zone
```

## Do not touch

- Header lockup: **CarveIntel** + `//` + screen title/tagline (blue bar, slashes, brand weight)
- Do not add hamburger until navigation IA is decided
- Do not add sticky “Start Your Order” CTA unless asked
- Do not redesign the hero/editorial layout casually
- Do not casually rewrite `report.html` pagination / cover / disclaimer logic (v6.3 recovered from live)

## Allowed polish (current)

- Stack `.section-list` (ABFTO sections) to **one column** below 768px — done in v2.2
- Homepage CTA points at `intake.html` (replaces broken `c2/FT-c3.html`)

## Local preview

```bash
cd sites/carveintel
python3 -m http.server 8080
```

Open:

- http://localhost:8080/
- http://localhost:8080/intake.html
- http://localhost:8080/walkthrough.html
- http://localhost:8080/report.html?token=DEMO_ASPIRIN

## Report data shape (OUT mapping later)

Demo / live jobs JSON use:

```json
{
  "molecule": "...",
  "report_type": "abfto",
  "customer_name": "...",
  "sections": [{ "id": "...", "title": "...", "content": "<html...>" }]
}
```

Aspirin demo sections (canonical complete example):

1. Executive Summary
2. Patent Landscape & Portfolio Analysis
3. Claim Architecture & Vulnerability Analysis
4. Jurisdictional Patent Topology
5. Biosimilar & Competitive Threat Assessment
6. Litigation Intelligence
7. Design-Around Opportunities & Strategic Options
8. Signal Detection & Market Intelligence
9. Strategic Verdict
10. Disclaimer & Methodology

Homepage marketing card still lists the 12-section ABFTO TOC (nice-to-have extras live here / in future bricks). Mapping intake → recon → these OUT sections is the next long job.

## Known issues

- Live origin homepage was **truncated mid-footer**; bootstrap closes footer/HTML cleanly
- `c2/FT-c3.html` remains 404 on live hosts — CTA now uses `intake.html`
- PHP backends (`validate.php`, job polling) are **not** in this repo; demo tokens load static JSON only
- Prefer a dedicated `philcheevers-pixel/carveintel` repo once the laptop source is found
