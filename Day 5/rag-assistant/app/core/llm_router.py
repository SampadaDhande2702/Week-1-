from __future__ import annotations

from dataclasses import dataclass

from app.core.llm_providers.base_provider import BaseLLMProvider
from app.utils.exceptions import FatalLLMError, ProviderUnavailableError


@dataclass(frozen=True)
class LLMResult:
    text: str
    provider_used: str
    fallback_triggered: bool


class LLMRouter:
    def __init__(self, providers: dict[str, BaseLLMProvider]) -> None:
        self._providers = providers

    def available(self) -> list[str]:
        out: list[str] = []
        for name, p in self._providers.items():
            try:
                if p.health_check():
                    out.append(name)
            except Exception:
                continue
        return out

    def generate_with_fallback(self, prompt: str, primary: str, fallback_chain: list[str]) -> LLMResult:
        order = [primary] + [p for p in fallback_chain if p != primary]
        last_err: Exception | None = None

        for i, name in enumerate(order):
            provider = self._providers.get(name)
            if provider is None:
                continue
            try:
                text = provider.generate(prompt)
                return LLMResult(text=text, provider_used=name, fallback_triggered=(i != 0))
            except ProviderUnavailableError as e:
                last_err = e
                continue
            except Exception as e:
                last_err = e
                continue

        raise FatalLLMError(f"All LLM providers failed. Last error: {last_err}")

