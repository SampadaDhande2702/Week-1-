from __future__ import annotations

from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    name: str

    @abstractmethod
    def generate(self, prompt: str) -> str: ...

    @abstractmethod
    def health_check(self) -> bool: ...

