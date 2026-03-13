from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    chunk_id: int
    text: str


def split_text(text: str, chunk_size: int = 1200, chunk_overlap: int = 200) -> list[Chunk]:
    """
    Simple character-based splitter with overlap.
    For 5-20 page PDFs this is reliable, fast, and good enough.
    """
    text = (text or "").strip()
    if not text:
        return []

    chunk_size = max(200, int(chunk_size))
    chunk_overlap = max(0, min(int(chunk_overlap), chunk_size - 1))

    chunks: list[Chunk] = []
    start = 0
    i = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        piece = text[start:end].strip()
        if piece:
            chunks.append(Chunk(chunk_id=i, text=piece))
            i += 1
        if end >= len(text):
            break
        start = max(0, end - chunk_overlap)

    # Drop very tiny chunks at the end (noise)
    if chunks and len(chunks[-1].text) < 80 and len(chunks) > 1:
        prev = chunks[-2]
        merged = (prev.text + "\n" + chunks[-1].text).strip()
        chunks[-2] = Chunk(chunk_id=prev.chunk_id, text=merged)
        chunks.pop()

    return chunks

