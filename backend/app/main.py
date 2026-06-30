"""Forja — backend FastAPI. Orquestra o grafo LangGraph e serve a API/SSE."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import catalog, runs, stream

app = FastAPI(title="Forja — Console do Pipeline", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(runs.router)
app.include_router(stream.router)
app.include_router(catalog.router)


@app.get("/health")
async def health():
    return {"ok": True}
