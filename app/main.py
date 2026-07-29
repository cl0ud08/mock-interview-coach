from fastapi import FastAPI

from app.api import health, sessions


app = FastAPI(title="Interview Coach", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Welcome to Interview Coach API"}


app.include_router(health.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")