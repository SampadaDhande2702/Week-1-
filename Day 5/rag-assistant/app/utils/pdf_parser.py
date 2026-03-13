from __future__ import annotations

import fitz  # PyMuPDF

from app.utils.exceptions import PDFEncryptedError, PDFNoTextError


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except fitz.FileDataError as e:
        raise PDFNoTextError("Invalid or unreadable PDF.") from e

    if doc.is_encrypted:
        raise PDFEncryptedError("PDF is encrypted / password-protected.")

    parts: list[str] = []
    for page in doc:
        text = page.get_text("text") or ""
        text = _clean(text)
        if text:
            parts.append(text)

    full = "\n\n".join(parts).strip()
    if not full:
        raise PDFNoTextError("No extractable text found (scanned/image-only PDF).")
    return full


def _clean(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.strip() for ln in s.split("\n")]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines).strip()

