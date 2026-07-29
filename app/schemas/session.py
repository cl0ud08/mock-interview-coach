from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class SessionStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    scoring = "scoring"
    complete = "complete"


class SessionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: str = Field(min_length=1, max_length=100)
    job_description: str | None = Field(default=None, max_length=5000)


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    job_description: str | None
    status: SessionStatus
    created_at: datetime
    question_count: int = 0