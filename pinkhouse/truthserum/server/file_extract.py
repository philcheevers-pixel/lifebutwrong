"""Extract plain text from uploaded files."""

from __future__ import annotations

import io
from pathlib import Path

from .limits import MAX_UPLOAD_BYTES


class FileExtractError(ValueError):
    pass


def extract_text_from_upload(filename: str, data: bytes) -> str:
    if len(data) > MAX_UPLOAD_BYTES:
        raise FileExtractError(
            f"File is too large ({len(data):,} bytes). Max is {MAX_UPLOAD_BYTES:,} bytes."
        )
    name = (filename or "upload.txt").lower()
    suffix = Path(name).suffix

    if suffix in {".txt", ".md", ".markdown", ".csv"}:
        return data.decode("utf-8", errors="replace")

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise FileExtractError("PDF support requires pypdf.") from exc
        reader = PdfReader(io.BytesIO(data))
        parts = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
        text = "\n".join(parts).strip()
        if not text:
            raise FileExtractError("Could not extract text from this PDF.")
        return text

    if suffix in {".docx"}:
        # Optional: lightweight XML scrape without python-docx dependency
        import re
        import zipfile

        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                xml = zf.read("word/document.xml").decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            raise FileExtractError("Could not read .docx file.") from exc
        text = re.sub(r"<w:p[^>]*>", "\n", xml)
        text = re.sub(r"<[^>]+>", "", text)
        text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        if not text:
            raise FileExtractError("Could not extract text from this Word document.")
        return text

    raise FileExtractError(
        "Unsupported file type. Use .txt, .md, .pdf, or .docx."
    )
