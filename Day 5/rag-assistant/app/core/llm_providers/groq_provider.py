from __future__ import annotations

import os
from typing import Any

import requests

from app.core.llm_providers.base_provider import BaseLLMProvider
from app.utils.exceptions import ProviderUnavailableError


class GroqProvider(BaseLLMProvider):
    """
    Minimal Groq provider via HTTPS (no extra SDK required).
    """

    name = "groq"

    def __init__(self, api_key: str | None, model: str) -> None:
        self._api_key = (api_key or os.getenv("GROQ_API_KEY") or "").strip()
        self._model = model
        if not self._api_key:
            raise ProviderUnavailableError("GROQ_API_KEY is not set.")

    def health_check(self) -> bool:
        return bool(self._api_key)

    def generate(self, prompt: str) -> str:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": self._model,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": "You are a helpful document assistant."},
                {"role": "user", "content": prompt},
            ],
        }
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=20)
        except requests.RequestException as e:
            raise ProviderUnavailableError(f"Groq request failed: {e}") from e

        if r.status_code >= 400:
            raise ProviderUnavailableError(f"Groq error {r.status_code}: {r.text[:300]}")

        data = r.json()
        return (data["choices"][0]["message"]["content"] or "").strip()

