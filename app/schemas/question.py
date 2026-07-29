from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Competency(str, Enum):
    technical = "technical"
    communication = "communication"
    problem_solving = "problem_solving"
    experience = "experience"


class QuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    competency: Competency
    difficulty: int = Field(ge=1, le=5)


class AnswerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: int
    transcript: str = Field(min_length=1, max_length=10_000)


class AnswerScore(BaseModel):
    score: float = Field(ge=0, le=10)
    feedback: str = Field(min_length=1, max_length=2000)
    competency: Competency