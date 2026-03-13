from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

from app.api.deps import session_store, settings
from app.core.embeddings import get_embedding_engine
from app.core.llm_providers.gemini_provider import GeminiProvider
from app.core.llm_providers.groq_provider import GroqProvider
from app.core.llm_providers.ollama_provider import OllamaProvider
from app.core.llm_router import LLMRouter
from app.core.rag_engine import RAGEngine
from app.utils.exceptions import FatalLLMError, ProviderUnavailableError


router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=8)
    query: str = Field(..., min_length=1)
    provider: str = Field("gemini")


@router.post("/chat")
async def chat(req: ChatRequest) -> dict:
    store = session_store.get(req.session_id)
    if store is None:
        raise HTTPException(status_code=404, detail="Session not found. Upload a PDF first.")

    providers = {}
    # Build providers lazily; missing keys just mean "unavailable".
    try:
        providers["gemini"] = GeminiProvider(settings.gemini_api_key, settings.gemini_model)
    except ProviderUnavailableError:
        pass
    try:
        providers["groq"] = GroqProvider(settings.groq_api_key, settings.groq_model)
    except ProviderUnavailableError:
        pass
    providers["ollama"] = OllamaProvider(settings.ollama_base_url)

    llm_router = LLMRouter(providers=providers)
    embeddings = get_embedding_engine(settings.embedding_model_name)
    rag = RAGEngine(embeddings=embeddings, store=store, llm_router=llm_router)

    fallback_chain = ["groq", "ollama"] if req.provider == "gemini" else ["gemini", "ollama"]
    # Always end with ollama as best-effort local fallback
    if "ollama" not in fallback_chain:
        fallback_chain.append("ollama")

    try:
        res = rag.answer(
            query=req.query,
            top_k=settings.top_k,
            primary_provider=req.provider,
            fallback_chain=fallback_chain,
        )
    except FatalLLMError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    return {
        "answer": res.answer,
        "provider_used": res.provider_used,
        "fallback_triggered": res.fallback_triggered,
        "sources": [
            {"chunk_id": s.chunk_id, "score": s.score, "text": s.text[:800]}
            for s in res.sources
        ],
    }

