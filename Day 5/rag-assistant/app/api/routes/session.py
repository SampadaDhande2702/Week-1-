from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.api.deps import session_store


router = APIRouter()


@router.delete("/session/{session_id}")
def delete_session(session_id: str) -> dict:
    ok = session_store.delete(session_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"status": "ok"}

