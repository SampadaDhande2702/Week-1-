from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from threading import Lock
from typing import Any
from uuid import uuid4


@dataclass
class SessionRecord:
    session_id: str
    store: Any


class SessionStore:
    def __init__(self, max_sessions: int = 3) -> None:
        self._max = max(1, int(max_sessions))
        self._lock = Lock()
        self._sessions: OrderedDict[str, SessionRecord] = OrderedDict()

    def create(self, store: Any) -> str:
        with self._lock:
            session_id = str(uuid4())
            self._sessions[session_id] = SessionRecord(session_id=session_id, store=store)
            self._sessions.move_to_end(session_id)
            self._evict_if_needed()
            return session_id

    def get(self, session_id: str) -> Any | None:
        with self._lock:
            rec = self._sessions.get(session_id)
            if rec is None:
                return None
            self._sessions.move_to_end(session_id)
            return rec.store

    def delete(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None

    def stats(self) -> dict[str, Any]:
        with self._lock:
            return {"active_sessions": len(self._sessions), "max_sessions": self._max}

    def _evict_if_needed(self) -> None:
        while len(self._sessions) > self._max:
            self._sessions.popitem(last=False)

