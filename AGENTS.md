# Agent playbook — Phil’s websites

Use this file every time you touch a site. Same steps, every domain.

## Golden rule

**No live site without a Git source of truth.**  
If the code is only on a laptop, droplet, or Cloudflare upload, stop and register it under `sites/` (or its own GitHub repo) before editing.

## Standard loop (do this every time)

1. **Identify the site** in [`sites/registry.yaml`](sites/registry.yaml).
2. **Open its `SITE.md`** (path listed in the registry). Read **Do not touch** before changing anything.
3. **Edit only the source path** in Git — never invent a parallel copy.
4. **Preview locally** (static: `python3 -m http.server` from the site folder).
5. **Commit + push + PR** on a `cursor/<name>-93d5` branch (or the run’s required branch pattern).
6. **Deploy** using the method in that site’s `SITE.md` (rsync / App Platform / Cloudflare / Squarespace).
7. **Verify** the live URL on desktop and a ~390px phone width.

## One card per site

Every site must have:

| Field | Purpose |
|---|---|
| Live URL | What visitors open |
| Source | GitHub repo + folder |
| Deploy | Exact command or platform |
| Do not touch | Brand/hero/checkout rules |
| Status | `git-backed` / `laptop-only` / `unknown` |

Template: copy [`sites/_template/SITE.md`](sites/_template/SITE.md).

## Hosting patterns we actually use

| Pattern | Where | How agents ship |
|---|---|---|
| **Pink House droplet** | `pinkhouse.tech` Apache on DigitalOcean | `rsync` site folder → `/var/www/html/<path>/` |
| **GitHub → App Platform** | e.g. Life But Wrong plan | Push `main`; static site autodeploy |
| **Squarespace** | `lifeofjesus.ca` commerce | Design may be mirrored elsewhere; **checkout stays on Squarespace** until cutover |
| **Cloudflare proxy** | e.g. `carveintel.com` | DNS at Cloudflare; origin is often the droplet — deploy origin, then purge CF cache if needed |

## Do / don’t

**Do**

- Look up the site in the registry first.
- Keep checkout / payment flows untouched unless the task says otherwise.
- Leave hero/brand lockups alone when `SITE.md` says so.
- Prefer small static HTML/CSS/JS unless the site already has a build step.

**Don’t**

- Edit a live URL by guessing source from another repo.
- Start a second copy of a site “just for now.”
- Add hamburger / sticky CTA / redesigns without an explicit ask.
- Mix unrelated brands into one homepage without a registry entry.

## Laptop homework (when source is missing)

If status is `laptop-only` or `unknown`:

1. On the laptop, find the project folder (search for the domain name or `index.html` title).
2. Create or open the GitHub repo named in the registry (or add the folder under `sites/<id>/`).
3. Push the real files.
4. Update `sites/registry.yaml` status to `git-backed`.
5. Only then ask an agent for UI/code changes.

## Quick start for a new site

```bash
cp -R sites/_template sites/<id>
# fill in sites/<id>/SITE.md
# add entry to sites/registry.yaml
# put source files in sites/<id>/ (or point SITE.md at another repo)
```
