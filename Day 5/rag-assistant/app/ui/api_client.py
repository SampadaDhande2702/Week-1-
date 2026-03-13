from __future__ import annotations

import requests


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self._base = base_url.rstrip("/")

    def health(self) -> dict:
        r = requests.get(f"{self._base}/health", timeout=10)
        r.raise_for_status()
        return r.json()

    def ingest_pdf(self, pdf_bytes: bytes, filename: str) -> dict:
        files = {"file": (filename, pdf_bytes, "application/pdf")}
        r = requests.post(f"{self._base}/ingest", files=files, timeout=120)
        r.raise_for_status()
        return r.json()

    def chat(self, session_id: str, query: str, provider: str) -> dict:
        payload = {"session_id": session_id, "query": query, "provider": provider}
        r = requests.post(f"{self._base}/chat", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()

