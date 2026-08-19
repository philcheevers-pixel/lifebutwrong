# Truth Serum — ready-to-build MVP

**Product:** free, experimental claim-level checker  
**Tone:** *Experimental automated claim review. Not a substitute for expert fact-checking. Built to surface issues, not to rubber-stamp documents.*  
**Brand home:** Pink House / Michelangelo posture demo — **not** Life But Wrong.

## What’s included

| Path | Role |
|------|------|
| `server/` | FastAPI backend (`POST /analyze`, rate limits, file upload) |
| `core/` | Claim extract → verify → traffic-light verdict → lean report |
| `web/` | Paste + file upload UI, results, download, Ko-fi support |
| `extension/` | Chrome Manifest V3 (selection / page → same API) |
| `cli.py` | Offline / scripted runs |

## Core loop

1. Accept pasted text or `.txt` / `.md` / `.pdf` / `.docx`
2. Extract atomic claims (LLM if `ANTHROPIC_API_KEY`, else heuristic)
3. Verify each claim (Brave Search if `BRAVE_API_KEY`, LLM judgment if key present, else heuristic)
4. Aggregate **Green / Yellow / Red** + lean exception-focused report
5. Optional voluntary support via **Ko-fi** on the results page only (never gated)

## Claim statuses

- Supported  
- Unsupported / weakly supported  
- Unclear / needs more context  
- Possible conflation or leap  

## MVP hard limits

- Max **3,000** words (env: `TRUTHSERUM_MAX_WORDS`)
- Max **40** claims (`TRUTHSERUM_MAX_CLAIMS`)
- **5** free runs / IP / day (`TRUTHSERUM_RATE_LIMIT_PER_DAY`)
- Upload max **2 MB**

## Run locally

```bash
cd pinkhouse/truthserum
python3 -m pip install -r requirements.txt
export PYTHONPATH=.
# optional: export ANTHROPIC_API_KEY=... BRAVE_API_KEY=...
python3 -m uvicorn server.app:app --host 0.0.0.0 --port 8080
```

Open http://127.0.0.1:8080/

CLI:

```bash
python3 cli.py --no-llm --no-search fixtures/sample_ai_text.txt
python3 tests/test_core.py
```

## Chrome extension

1. Start the backend
2. Chrome → Extensions → Load unpacked → select `extension/`
3. Set API base in the popup (default `http://127.0.0.1:8080`)
4. Select text on a page → right-click **Check with Truth Serum**

For a public droplet URL, set the popup API base to `https://your.domain` and ensure CORS allows the extension origin (or serve API on the same host).

## Deploy (DigitalOcean droplet)

```bash
git pull
cd pinkhouse/truthserum
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# put secrets in /etc/truthserum.env
uvicorn server.app:app --host 0.0.0.0 --port 8080
```

Put nginx in front (TLS), set `ANTHROPIC_API_KEY`, `BRAVE_API_KEY`, and update the Ko-fi URL in `web/app.js` / extension storage.

## Ko-fi

Edit `web/app.js` (`TRUTHSERUM_KOFI_URL` or the default href) and the extension popup link to your Ko-fi page. Support appears **only on results**.

## Done checklist (v1)

- [x] Web paste + file upload
- [x] Traffic-light results + exception list
- [x] Downloadable Markdown/HTML report
- [x] Chrome extension → same backend
- [x] Ko-fi button on results
- [x] Word / claim / rate limits
- [ ] Wire real Ko-fi URL + API keys on droplet
- [ ] Point DNS / nginx at the service
