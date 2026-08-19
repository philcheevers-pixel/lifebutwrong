"""
Truth Serum FastAPI backend.

Run:
  cd pinkhouse/truthserum
  PYTHONPATH=. uvicorn server.app:app --host 0.0.0.0 --port 8080
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.pipeline import analyze_text  # noqa: E402
from server.file_extract import FileExtractError, extract_text_from_upload  # noqa: E402
from server.limits import MAX_CLAIMS, MAX_WORDS, enforce_text_limits  # noqa: E402
from server.rate_limit import check_rate_limit  # noqa: E402

app = FastAPI(
    title="Truth Serum",
    description="Experimental automated claim review.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("TRUTHSERUM_CORS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

WEB_DIR = ROOT / "web"
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "truthserum",
        "max_words": MAX_WORDS,
        "max_claims": MAX_CLAIMS,
        "brave": bool(os.environ.get("BRAVE_API_KEY") or os.environ.get("BRAVE_SEARCH_API_KEY")),
        "llm": bool(os.environ.get("ANTHROPIC_API_KEY")),
    }


@app.get("/", response_class=HTMLResponse)
def index():
    index_path = WEB_DIR / "index.html"
    if not index_path.exists():
        return HTMLResponse("<h1>Truth Serum</h1><p>Web UI missing.</p>")
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


@app.post("/analyze")
async def analyze(
    request: Request,
    text: str | None = Form(None),
    file: UploadFile | None = File(None),
):
    # Also accept JSON body for the extension
    if text is None and file is None:
        try:
            body = await request.json()
        except Exception:  # noqa: BLE001
            body = {}
        if isinstance(body, dict):
            text = body.get("text")

    ip = _client_ip(request)
    allowed, remaining = check_rate_limit(ip)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Daily free-run limit reached for this network. Try again tomorrow.",
        )

    source_text = (text or "").strip()
    if file is not None and file.filename:
        data = await file.read()
        try:
            source_text = extract_text_from_upload(file.filename, data)
        except FileExtractError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    err = enforce_text_limits(source_text)
    if err:
        raise HTTPException(status_code=400, detail=err)

    result = analyze_text(source_text, max_claims=MAX_CLAIMS)
    payload = result.model_dump()
    payload["rate_limit_remaining"] = remaining
    return JSONResponse(payload)


@app.post("/report.md")
async def report_md(request: Request):
    data = await request.json()
    text = (data or {}).get("text") or ""
    err = enforce_text_limits(text)
    if err:
        raise HTTPException(status_code=400, detail=err)
    result = analyze_text(text, max_claims=MAX_CLAIMS)
    return PlainTextResponse(
        result.report_markdown,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="truth-serum-report.md"'},
    )


@app.post("/report.html")
async def report_html(request: Request):
    data = await request.json()
    text = (data or {}).get("text") or ""
    err = enforce_text_limits(text)
    if err:
        raise HTTPException(status_code=400, detail=err)
    result = analyze_text(text, max_claims=MAX_CLAIMS)
    return Response(
        result.report_html,
        media_type="text/html; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="truth-serum-report.html"'},
    )
