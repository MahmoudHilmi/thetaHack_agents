from fastapi import FastAPI
from oracle.config import settings

app = FastAPI(title="ORACLE", version="0.1.0")


@app.get("/health")
async def health() -> dict:
    """Health-check endpoint for production readiness monitoring."""
    return {"status": "ok"}


@app.get("/")
async def root() -> dict:
    return {"service": "ORACLE", "ready": True if settings.OPENAI_API_KEY else False}
