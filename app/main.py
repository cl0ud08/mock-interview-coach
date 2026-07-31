from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import health, sessions
from app.database import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)   # temporary — replaced by Alembic on D4
    yield


app = FastAPI(title="Interview Coach", version="0.1.0", lifespan=lifespan)

app.include_router(health.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")