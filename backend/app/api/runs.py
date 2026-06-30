"""Rotas de runs: criar, listar, detalhar, aprovar/rejeitar/regenerar."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..events import bus
from ..pipeline.state import slugify
from .. import runner

router = APIRouter()


class NovoRun(BaseModel):
    tema: str = Field(..., min_length=1)
    metafora: str = Field(..., min_length=1)
    max_tentativas: int = 3
    hitl: bool = True


@router.post("/runs")
async def criar_run(body: NovoRun):
    slug = slugify(body.tema, body.metafora)
    if bus.get(slug) and bus.get(slug).status in ("Em execução", "Aguardando aprovação"):
        raise HTTPException(409, f"Já existe um run ativo para o slug '{slug}'.")
    thread_id = runner.start_run(body.tema, body.metafora, slug,
                                 body.max_tentativas, body.hitl)
    return {"thread_id": thread_id, "slug": slug}


@router.get("/runs")
async def listar_runs():
    return {"runs": bus.list()}


@router.get("/runs/{thread_id}")
async def detalhar_run(thread_id: str):
    run = bus.get(thread_id)
    if not run:
        raise HTTPException(404, "Run não encontrado.")
    return run.to_detail()


@router.post("/runs/{thread_id}/approve")
async def aprovar(thread_id: str):
    if not bus.get(thread_id):
        raise HTTPException(404, "Run não encontrado.")
    await runner.approve_run(thread_id)
    return {"ok": True, "status": bus.get(thread_id).status}


@router.post("/runs/{thread_id}/reject")
async def rejeitar(thread_id: str):
    if not bus.get(thread_id):
        raise HTTPException(404, "Run não encontrado.")
    await runner.reject_run(thread_id)
    return {"ok": True}


@router.post("/runs/{thread_id}/regenerate")
async def regenerar(thread_id: str):
    if not bus.get(thread_id):
        raise HTTPException(404, "Run não encontrado.")
    await runner.regenerate_run(thread_id)
    return {"ok": True}
