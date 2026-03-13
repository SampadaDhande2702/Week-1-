import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    groq_api_key: str | None
    gemini_api_key: str | None
    ollama_base_url: str

    embedding_model_name: str
    groq_model: str
    gemini_model: str

    chunk_size: int
    chunk_overlap: int
    top_k: int


def get_settings() -> Settings:
    load_dotenv()

    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip()
    if not ollama_base_url:
        ollama_base_url = "http://localhost:11434"

    return Settings(
        groq_api_key=_maybe(os.getenv("GROQ_API_KEY")),
        gemini_api_key=_maybe(os.getenv("GEMINI_API_KEY")),
        ollama_base_url=ollama_base_url,
        embedding_model_name=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
        groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        chunk_size=int(os.getenv("CHUNK_SIZE", "1200")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "200")),
        top_k=int(os.getenv("TOP_K", "4")),
    )


def _maybe(v: str | None) -> str | None:
    if v is None:
        return None
    v = v.strip()
    return v or None

