from __future__ import annotations

import os
from typing import Any

import requests

from app.core.llm_providers.base_provider import BaseLLMProvider
from app.utils.exceptions import ProviderUnavailableError


class GeminiProvider(BaseLLMProvider):
    """
    Minimal Gemini provider via REST.
    Uses the Google Generative Language API endpoint format.
    """

    name = "gemini"

    def __init__(self, api_key: str | None, model: str) -> None:
        self._api_key = (api_key or os.getenv("GEMINI_API_KEY") or "").strip()
        self._model = model
        if not self._api_key:
            raise ProviderUnavailableError("GEMINI_API_KEY is not set.")

    def health_check(self) -> bool:
        return bool(self._api_key)

    def generate(self, prompt: str) -> str:
        # v1beta endpoint used by many examples; good enough for this starter app
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self._model}:generateContent"
        params = {"key": self._api_key}
        payload: dict[str, Any] = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }
        try:
            r = requests.post(url, params=params, json=payload, timeout=20)
        except requests.RequestException as e:
            raise ProviderUnavailableError(f"Gemini request failed: {e}") from e

        if r.status_code >= 400:
            raise ProviderUnavailableError(f"Gemini error {r.status_code}: {r.text[:300]}")

        data = r.json()
        try:
            parts = data["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts)
            return text.strip()
        except Exception as e:
            raise ProviderUnavailableError("Gemini response format unexpected.") from e

