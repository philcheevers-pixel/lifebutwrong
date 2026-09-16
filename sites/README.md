# Sites registry

This folder is the **map** of Phil’s websites so every Cursor agent does the same thing.

| Start here | Purpose |
|---|---|
| [`../AGENTS.md`](../AGENTS.md) | Repeatable edit → PR → deploy loop |
| [`registry.yaml`](registry.yaml) | Machine-readable inventory |
| `_template/` | Copy when adding a new site |
| `<id>/SITE.md` | Per-site rules and deploy notes |

## Current bootstrap in this repo

| Folder | Site |
|---|---|
| `carveintel/` | Recovered CarveIntel homepage + mobile ABFTO stack |
| `../lifeofjesus/` | Life of Jesus pinkhouse testbed (already at repo root) |
| `../` (root) | Life But Wrong static site |

## Laptop checklist (CarveIntel and anything `unknown`)

When you have the laptop open:

1. Search for the real project (`CarveIntel`, `index.html`, `ABFTO`).
2. Diff it against `sites/carveintel/` — if the laptop copy is newer/complete, replace the bootstrap.
3. Prefer creating `github.com/philcheevers-pixel/carveintel` and moving the folder there; update `registry.yaml`.
4. Confirm droplet path `/var/www/html/carveintel/` and Cloudflare DNS for `carveintel.com`.
5. Fix or remove the broken `c2/FT-c3.html` order link when you are ready.
