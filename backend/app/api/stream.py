"""SSE: emite os eventos do grafo em tempo real para a tela Console."""
from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse

from ..events import bus

router = APIRouter()


@router.get("/runs/{thread_id}/stream")
async def stream(thread_id: str, request: Request):
    if not bus.get(thread_id):
        raise HTTPException(404, "Run não encontrado.")
    q = bus.subscribe(thread_id)

    async def gen():
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    ev = await asyncio.wait_for(q.get(), timeout=15.0)
                    yield {"event": "node", "data": json.dumps(ev, ensure_ascii=False)}
                except asyncio.TimeoutError:
                    yield {"event": "ping", "data": "{}"}  # keep-alive
        finally:
            bus.unsubscribe(thread_id, q)

    return EventSourceResponse(gen())
