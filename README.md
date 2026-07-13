# Life But Wrong

Static site for **lifebutwrong.com** — satirical wrong takes, inappropriate products, and a separate factual works page.

## Local preview

Open `index.html` in a browser, or run a simple server:

```bash
npx serve .
```

## Your launch checklist

### 1. GitHub (after agent push)

- [ ] Confirm repo exists on GitHub
- [ ] Confirm `main` branch has all site files

### 2. DigitalOcean App Platform

1. Dashboard → **Apps** → **Create App**
2. Connect **GitHub** → select this repo
3. Branch: `main`
4. Component: **Static Site**
5. Build command: leave empty
6. Output directory: `/`
7. Enable **Autodeploy** on push
8. Deploy and open the `*.ondigitalocean.app` URL

### 3. DigitalOcean DNS (replace HostGator)

1. **Networking** → **Domains** → Add `lifebutwrong.com`
2. App → **Settings** → **Domains** → Add `lifebutwrong.com` and `www.lifebutwrong.com`
3. Copy DigitalOcean nameservers
4. **Network Solutions** → change nameservers from HostGator to DigitalOcean
5. No MX records needed (no email on this domain)
6. Verify `https://lifebutwrong.com` then cancel HostGator

### 4. Replace placeholder shop links

Search the repo for `YOUR-` and replace:

| Placeholder | Replace with |
|-------------|--------------|
| `YOUR-PRINTFUL-STORE.com` | Your Printful/Etsy/Shopify store URLs |
| `YOUR-NAME.gumroad.com` | Your Gumroad product links |
| `YOUR-ASIN-HERE` | Amazon book ASINs |
| `YOUR-AFFILIATE-TAG-20` | Amazon Associates tag (optional) |

Files to edit: `shop.html`, `works/index.html`

### 5. Gumroad — AI History pamphlet

- [ ] Create or confirm product on Gumroad
- [ ] Paste URL into `works/index.html`
- [ ] Suggested price: $7–12 PDF

### 6. Amazon books

- [ ] Add real titles, descriptions, and `/dp/ASIN` links in `works/index.html`
- [ ] Optional: join Amazon Associates for `?tag=` affiliate links

### 7. Newsletter

- [ ] Create Beehiiv or Substack list ("Wrong Weekly")
- [ ] Replace the placeholder form in `index.html` with embed code

### 8. Stripe (later)

Not required for launch. Use Gumroad and Printful first. Add Stripe Checkout when you want payments on your own domain.

### 9. Promote

- [ ] Pinterest: quote pins from the five posts
- [ ] X: one wrong take per day for a week
- [ ] Link shop from every post footer

## Site structure

```
index.html              Homepage
shop.html               Joke merch + digital products
works/index.html        Factual books (AI pamphlet, Amazon)
posts/*.html            Five starter wrong-take articles
css/style.css           Institutional ironic styling
js/main.js              Newsletter placeholder handler
```

## Cursor mode tip

If you do not see Ask/Agent dropdown: you are usually already in the right mode for the chat you are using. **Ctrl+I** opens Composer; **Ctrl+L** opens a new chat. This project was built in Agent mode.
