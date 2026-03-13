from __future__ import annotations

from dataclasses import dataclass

import faiss
import numpy as np

from app.utils.exceptions import IndexNotReadyError
from app.utils.text_splitter import Chunk


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: int
    text: str
    score: float


class FAISSStore:
    def __init__(self) -> None:
        self._index: faiss.Index | None = None
        self._chunks: dict[int, Chunk] = {}

    @property
    def size(self) -> int:
        return len(self._chunks)

    def build(self, vectors: np.ndarray, chunks: list[Chunk]) -> None:
        if vectors.ndim != 2:
            raise ValueError("vectors must be a 2D array")
        if len(chunks) != vectors.shape[0]:
            raise ValueError("vectors/chunks length mismatch")

        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)  # embeddings are normalized -> IP ~ cosine similarity
        index.add(vectors)

        self._index = index
        self._chunks = {c.chunk_id: c for c in chunks}

    def search(self, query_vector: np.ndarray, k: int = 4) -> list[RetrievedChunk]:
        if self._index is None:
            raise IndexNotReadyError("Index not built yet.")
        if query_vector.ndim != 1:
            raise ValueError("query_vector must be 1D")

        total = len(self._chunks)
        if total == 0:
            return []

        k = max(1, min(int(k), total))
        q = query_vector.astype("float32")[None, :]
        scores, ids = self._index.search(q, k)

        out: list[RetrievedChunk] = []
        for score, idx in zip(scores[0].tolist(), ids[0].tolist()):
            if idx < 0:
                continue
            chunk = self._chunks.get(idx)
            if chunk is None:
                continue
            out.append(RetrievedChunk(chunk_id=chunk.chunk_id, text=chunk.text, score=float(score)))
        return out

