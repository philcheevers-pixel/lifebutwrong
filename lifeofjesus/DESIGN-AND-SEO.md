# Life of Jesus — Design mindset & SEO notes

This document explains **why the testbed looks the way it does**, and **what SEO is already in place** (plus what is intentionally not there yet).

**Live preview:** https://pinkhouse.tech/lifeofjesus/  
**Checkout today:** Buy buttons still open the live Squarespace shop at [lifeofjesus.ca](https://www.lifeofjesus.ca/).

---

## 1. Design mindset

### One sentence

Make a **quiet gallery for a comfort gift** — not a hard-sell shop — so visitors feel the art and the story before they think about price.

### Guiding ideas

| Idea | What it means on the page |
|---|---|
| **Comfort first, shop second** | Hero is brand + one line + short support + CTAs. No price grid, schedule, or promo clutter in the first viewport. |
| **Brand as the hero** | “Life of Jesus” is the big signal. The headline never overpowers the brand. |
| **Gallery calm** | Cool stone light, antique gold accents, soft mist/paper gradients — museum quiet, not flashy commerce. |
| **Real art as the anchor** | Full-bleed sacred art in the hero; linger sections show open pages. Decorative gradients alone are not the idea. |
| **One job per section** | Home → linger with art → products → gift occasions → social proof. Each block has one purpose. |
| **Cards only when shopping** | Product tiles are interactive shop containers. The hero and story sections are not card layouts. |
| **Motion with presence** | Slow hero drift, rise-in copy, and scroll reveals. Enough life to feel cared for; nothing noisy. |

### Visual system (CSS variables)

- **Ink / slate** for readable text and quiet structure (`#1a222c` family)
- **Mist → paper → gallery** cool greys for atmosphere
- **Antique gold** (`#8f7348` / `#6e5734`) for accent and warmth
- **Fonts:** Cormorant Garamond (display/brand), Literata (body), Figtree (UI)

### Page map

| Page | Job |
|---|---|
| `index.html` | Brand, comfort, gift framing |
| `shop.html` | Books + bundles |
| `book/` | Hero product + look-inside |
| `about.html` | Mission + testimonials |
| `contact.html` | Press vs church/charity paths |

### Audience framing

Families, gift-givers, Canadian churches/parishes, pastoral care, fundraisers. Tone is **broad Christian + classical art** — welcoming, not denominational hard-sell.

---

## 2. SEO elements already on the site

SEO here is **on-page and social-share ready**. It is not a full technical SEO stack yet (no sitemap/robots/schema). That is fine for a Pink House testbed; add the missing pieces before or at DNS cutover to `lifeofjesus.ca`.

### On every Life of Jesus page

| Element | Purpose |
|---|---|
| `<html lang="en-CA">` | Tells search engines / browsers this is Canadian English. |
| Unique `<title>` | Primary result title in Google; brand + page intent. |
| Unique `meta description` | Snippet under the title in search results. |
| `link rel="canonical"` | Points to the preferred URL on `pinkhouse.tech/lifeofjesus/…` so duplicates don’t split signal. |
| Semantic HTML | `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, headings in order. |
| Image `alt` text | Describes product/linger images for accessibility and image search; decorative hero image uses empty `alt` on purpose. |
| Google Fonts `preconnect` | Faster font load (performance helps SEO indirectly). |

### Open Graph (Facebook / iMessage / LinkedIn previews)

| Page | OG tags |
|---|---|
| Home | Full set: title, description, type, url, image (`jesus-cover.webp`) |
| Shop | title, description, image (`bundle-trio.webp`) |
| Book | title, description, image (`jesus-cover.webp`) |
| About / Contact | Titles + descriptions + canonicals; **no OG tags yet** |

When someone shares a link, these tags control the preview title, blurb, and image.

### What is *not* in the repo yet (recommended before going fully live)

| Missing piece | Why add it |
|---|---|
| `robots.txt` | Tell crawlers what they may index. |
| `sitemap.xml` | Help Google discover all pages quickly. |
| JSON-LD (Product / Organization / WebSite) | Richer search results (price, availability, brand). |
| Twitter / X card tags | Cleaner previews on X. |
| Favicon / apple-touch-icon | Trust and brand in browser tabs and bookmarks. |
| Complete OG on About & Contact | Consistent sharing from every URL. |
| Fix dual `<h1>` on `book/` | One clear H1 per page is cleaner for SEO. |

When the domain moves to `lifeofjesus.ca`, **update every canonical and `og:url` / `og:image`** to the new host.

### Keyword / content mindset (not keyword stuffing)

Copy was written around natural phrases people actually search or say:

- Life of Jesus coloring book  
- sacred art / classical Christian art  
- Christian gift / parish / family  
- Caravaggio, Rubens, Last Supper  
- comfort, study, gift-giving  

Headings describe real sections (“Familiar scenes. Room to breathe.”) rather than stuffing “best Christian coloring book 2026” into every line. Trust and clarity win for this audience.

---

## 3. Study guide — marketing recommendation

There is **no study guide page or PDF on this site yet**. The site only hints that the books support comfort, **study**, and gift-giving.

### Recommendation

**Yes — distribute the study guide from this site.** Because it costs nothing to give away, treat it as a **ministry/gift asset**, not only a paid add-on.

Best default strategy:

1. **Free sample or short guide on the site** (PDF download or “Study with the book” page)  
   - Builds trust for churches, grandparents, and gift buyers  
   - Gives Google more useful text to index  
   - Supports parish/fundraiser conversations without a hard sell  

2. **Full study guide free with purchase** (or clearly linked from the order confirmation / product page on Squarespace)  
   - Rewards buyers without raising cost of goods  
   - Makes the $39.99 book feel like a complete experience  

3. **Optional: email gate only if you want a list**  
   - “Get the study guide” → name/email → PDF  
   - Useful for Mark/Pierre marketing later; skip the gate if the goal is maximum parish adoption  

### What I would *not* do first

- Hide the entire guide behind purchase if churches are a key channel — pastors often need to evaluate materials before ordering.  
- Drop a huge PDF with no landing page — give it a short page with one headline, one paragraph, and a download/CTA next to the book.

### Simple next build (when you want it)

- A page like `/study-guide/` (or a section on About)  
- 1–2 sample lessons or a short PDF  
- CTA: “Shop the book” + “Download the guide”  
- Later: Product schema + sitemap once the guide URL exists  

---

## 4. How this fits the business setup

- **Experience / design** lives on Pink House (`pinkhouse.tech/lifeofjesus/`).  
- **Money** still happens on Squarespace (`lifeofjesus.ca`).  
- The **“Testbed preview”** banner makes that honest so nobody is confused during review.  
- After Mark and Pierre comment, typical next steps are: polish copy → add study guide if desired → finish technical SEO → then DNS cutover, Squarespace port, or Stripe.

---

## 5. Quick checklist for “going live”

- [ ] Collect Mark / Pierre comments and apply them  
- [ ] Decide study-guide distribution (free sample vs with purchase vs both)  
- [ ] Add sitemap, robots, favicon, JSON-LD  
- [ ] Fill OG tags on About & Contact  
- [ ] Point canonicals / OG URLs at the final domain  
- [ ] Confirm every Buy button still hits the correct Squarespace product  

---

*Written for the Pink House Life of Jesus testbed so the team has a shared record of design intent and SEO choices.*
