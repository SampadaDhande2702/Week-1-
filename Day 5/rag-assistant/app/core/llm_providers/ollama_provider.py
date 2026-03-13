from __future__ import annotations

from typing import Any

import requests

from app.core.llm_providers.base_provider import BaseLLMProvider
from app.utils.exceptions import ProviderUnavailableError


class OllamaProvider(BaseLLMProvider):
    name = "ollama"

    def __init__(self, base_url: str, model: str = "llama3") -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model

    def health_check(self) -> bool:
        try:
            r = requests.get(f"{self._base_url}/api/tags", timeout=3)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def generate(self, prompt: str) -> str:
        url = f"{self._base_url}/api/generate"
        payload: dict[str, Any] = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
        }
        try:
            r = requests.post(url, json=payload, timeout=60)
        except requests.RequestException as e:
            raise ProviderUnavailableError(f"Ollama request failed: {e}") from e

        if r.status_code >= 400:
            raise ProviderUnavailableError(f"Ollama error {r.status_code}: {r.text[:300]}")

        data = r.json()
        return (data.get("response") or "").strip()

