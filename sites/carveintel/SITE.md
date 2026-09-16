# CarveIntel

Pharmaceutical patent intelligence — ABFTO reports.

## Identity

- **Live URLs:** https://carveintel.com/ · mirror https://pinkhouse.tech/carveintel/
- **Source path:** `sites/carveintel/` in `philcheevers-pixel/lifebutwrong` (bootstrap)
- **Status:** `git-backed-bootstrap` — recovered from live on 2026-09-16; confirm against laptop copy

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

## Allowed polish (current)

- Stack `.section-list` (ABFTO sections) to **one column** below 768px — done in v2.2

## Local preview

```bash
cd sites/carveintel
python3 -m http.server 8080
```

Open http://localhost:8080/

## Known issues

- Live origin file was **truncated mid-footer**; bootstrap closes footer/HTML cleanly
- `c2/FT-c3.html` (“Start Your Order”) returns **404** on both hosts
- Prefer a dedicated `philcheevers-pixel/carveintel` repo once the laptop source is found
