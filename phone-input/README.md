# Phone input (word drop)

A one-job phone page: put words down before they leave, and keep them when the window changes.

## What it does

- Large type, phone-first layout
- Auto-saves to `localStorage` on this device
- Restores on reopen
- Copy / Colour (yellow page) / Clear
- Nothing is uploaded

## Local preview

```bash
cd phone-input
python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/` on desktop, or your LAN IP on a phone.

## Deploy note

Mirror this folder to the Pink House host when ready (same pattern as other static Pink House pages). Until then, this PR is the source.
