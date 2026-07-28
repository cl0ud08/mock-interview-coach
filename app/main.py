from fastapi import FastAPI

from app.api import health

app = FastAPI(title="Interview Coach", version="0.1.0")

app.include_router(health.router, prefix="/api")