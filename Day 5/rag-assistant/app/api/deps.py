from __future__ import annotations

from app.api.session_store import SessionStore
from config import get_settings


settings = get_settings()
session_store = SessionStore(max_sessions=3)

