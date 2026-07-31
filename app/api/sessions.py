from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app.database import get_db
from app.models import Session as SessionModel
from app.schemas.session import SessionCreate, SessionOut

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionCreate, db: DbSession = Depends(get_db)) -> SessionOut:
    session = SessionModel(role=payload.role, job_description=payload.job_description)
    db.add(session)
    db.commit()
    db.refresh(session)          # reload so id and created_at are populated
    return SessionOut.model_validate(session)


@router.get("", response_model=list[SessionOut])
def list_sessions(db: DbSession = Depends(get_db)) -> list[SessionOut]:
    rows = db.execute(select(SessionModel).order_by(SessionModel.created_at.desc())).scalars().all()
    return [SessionOut.model_validate(r) for r in rows]


@router.get("/{session_id}", response_model=SessionOut)
def get_session(session_id: int, db: DbSession = Depends(get_db)) -> SessionOut:
    session = db.get(SessionModel, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionOut.model_validate(session)