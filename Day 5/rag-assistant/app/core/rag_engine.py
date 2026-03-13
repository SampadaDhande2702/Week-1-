from __future__ import annotations

from dataclasses import dataclass

from app.core.embeddings import EmbeddingEngine
from app.core.llm_router import LLMResult, LLMRouter
from app.db.faiss_store import FAISSStore, RetrievedChunk


@dataclass(frozen=True)
class RAGResponse:
    answer: str
    sources: list[RetrievedChunk]
    provider_used: str
    fallback_triggered: bool


class RAGEngine:
    def __init__(self, embeddings: EmbeddingEngine, store: FAISSStore, llm_router: LLMRouter) -> None:
        self._embeddings = embeddings
        self._store = store
        self._llm = llm_router

    def answer(self, query: str, top_k: int, primary_provider: str, fallback_chain: list[str]) -> RAGResponse:
        qv = self._embeddings.embed_query(query)
        hits = self._store.search(qv, k=top_k)
        prompt = _build_prompt(query=query, hits=hits)
        llm_res: LLMResult = self._llm.generate_with_fallback(
            prompt=prompt,
            primary=primary_provider,
            fallback_chain=fallback_chain,
        )
        return RAGResponse(
            answer=llm_res.text,
            sources=hits,
            provider_used=llm_res.provider_used,
            fallback_triggered=llm_res.fallback_triggered,
        )


def _build_prompt(query: str, hits: list[RetrievedChunk]) -> str:
    context = "\n\n---\n\n".join(f"[chunk {h.chunk_id} | score {h.score:.3f}]\n{h.text}" for h in hits)
    return (
        "You are a document assistant. Answer ONLY from the provided context.\n"
        'If the answer is not in the context, say "I don\'t know."\n\n'
        f"CONTEXT:\n{context}\n\n"
        f"USER QUESTION:\n{query}\n"
    )

