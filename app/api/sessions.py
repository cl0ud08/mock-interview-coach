from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from app.schemas.session import SessionCreate, SessionOut, SessionStatus

router = APIRouter(prefix="/sessions", tags=["sessions"])

# Temporary in-memory store — replaced by Postgres on D3.
_sessions: dict[int, dict] = {}
_next_id = 1


@router.post("", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionCreate) -> SessionOut:
    global _next_id
    record = {
        "id": _next_id,
        "role": payload.role,
        "job_description": payload.job_description,
        "status": SessionStatus.created,
        "created_at": datetime.now(timezone.utc),
        "question_count": 0,
    }
    _sessions[_next_id] = record
    _next_id += 1
    return SessionOut(**record)


@router.get("", response_model=list[SessionOut])
def list_sessions() -> list[SessionOut]:
    return [SessionOut(**r) for r in _sessions.values()]


@router.get("/{session_id}", response_model=SessionOut)
def get_session(session_id: int) -> SessionOut:
    record = _sessions.get(session_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionOut(**record)