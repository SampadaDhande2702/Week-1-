from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.api.deps import session_store, settings
from app.core.embeddings import get_embedding_engine
from app.db.faiss_store import FAISSStore
from app.utils.exceptions import PDFEncryptedError, PDFNoTextError
from app.utils.pdf_parser import extract_text_from_pdf_bytes
from app.utils.text_splitter import split_text


router = APIRouter()


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)) -> dict:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    pdf_bytes = await file.read()
    try:
        text = extract_text_from_pdf_bytes(pdf_bytes)
    except PDFEncryptedError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except PDFNoTextError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    chunks = split_text(text, chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
    if not chunks:
        raise HTTPException(status_code=400, detail="No text chunks produced from this PDF.")

    engine = get_embedding_engine(settings.embedding_model_name)
    vectors = engine.embed_texts([c.text for c in chunks])

    store = FAISSStore()
    store.build(vectors=vectors, chunks=chunks)

    session_id = session_store.create(store)
    return {"status": "ok", "session_id": session_id, "chunk_count": len(chunks)}

