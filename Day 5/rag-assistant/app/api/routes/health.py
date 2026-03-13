from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import session_store, settings
from app.core.llm_providers.gemini_provider import GeminiProvider
from app.core.llm_providers.groq_provider import GroqProvider
from app.core.llm_providers.ollama_provider import OllamaProvider
from app.utils.exceptions import ProviderUnavailableError


router = APIRouter()


@router.get("/health")
def health() -> dict:
    providers: dict[str, bool] = {}
    try:
        providers["gemini"] = GeminiProvider(settings.gemini_api_key, settings.gemini_model).health_check()
    except ProviderUnavailableError:
        providers["gemini"] = False
    try:
        providers["groq"] = GroqProvider(settings.groq_api_key, settings.groq_model).health_check()
    except ProviderUnavailableError:
        providers["groq"] = False
    providers["ollama"] = OllamaProvider(settings.ollama_base_url).health_check()

    return {
        "status": "ok",
        "sessions": session_store.stats(),
        "providers": providers,
    }

