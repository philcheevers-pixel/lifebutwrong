# Life of Jesus — Pink House testbed

Comfort-first website for Pierre’s **Life of Jesus** coloring books.

**Target URL:** `https://pinkhouse.tech/lifeofjesus/`  
**Checkout:** Buy buttons send visitors to the live Squarespace store at `lifeofjesus.ca` (no wipe, no Stripe rebuild yet).

## What’s in this folder

| Path | Purpose |
|---|---|
| `index.html` | Comfort homepage (brand + art + gift framing) |
| `shop.html` | Books + bundles |
| `book/` | Hero product page with look-inside thumbs |
| `about.html` | Mission + testimonials |
| `contact.html` | Press / church contacts |
| `css/`, `js/`, `assets/` | Styles, motion, product imagery |

## Local preview

From this folder:

```bash
cd lifeofjesus
python3 -m http.server 8080
```

Open `http://localhost:8080/`.

## Deploy to pinkhouse.tech

This is a static site for Apache. Copy the **contents** of this folder to the web root path `/lifeofjesus/` on the Pink House droplet.

Example (from a machine that has SSH access):

```bash
# adjust user/host/path to your droplet docroot
rsync -av --delete ./lifeofjesus/ USER@pinkhouse.tech:/var/www/html/lifeofjesus/
```

Then visit:

- https://pinkhouse.tech/lifeofjesus/
- https://pinkhouse.tech/lifeofjesus/shop.html
- https://pinkhouse.tech/lifeofjesus/book/

No build step. No Node required.

## Next cutover options (later)

1. Point `lifeofjesus.ca` DNS at this site, **or**
2. Port the approved design back into Squarespace, **or**
3. Add Stripe Checkout here and retire Squarespace commerce.
