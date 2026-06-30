"""Orquestra o grafo: dispara em background, detecta o interrupt (HITL) e retoma."""
from __future__ import annotations

import asyncio
from typing import Optional

import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from .config import settings
from .events import (Run, bus, RUN_AGUARDANDO, RUN_CONCLUIDO, RUN_EM_EXEC, RUN_FALHA)
from .pipeline.graph import build_graph

# Checkpointer assíncrono persistente por thread_id (resume cruza requisições / restart).
# Construído preguiçosamente dentro do event loop (aiosqlite exige loop ativo).
_graph = None
_graph_lock = asyncio.Lock()


async def get_graph():
    global _graph
    if _graph is None:
        async with _graph_lock:
            if _graph is None:
                conn = await aiosqlite.connect(settings().db_path)
                _graph = build_graph(AsyncSqliteSaver(conn))
    return _graph


def _config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


async def _drive(thread_id: str, payload: Optional[dict]) -> None:
    """Roda/retoma o grafo até o próximo ponto de parada (interrupt ou END)."""
    config = _config(thread_id)
    run = bus.get(thread_id)
    graph = await get_graph()
    try:
        async for _ in graph.astream(payload, config, stream_mode="updates"):
            snap = await graph.aget_state(config)
            if run and snap.values.get("tentativas_correcao") is not None:
                run.tentativas = snap.values["tentativas_correcao"]

        snap = await graph.aget_state(config)
        nxt = snap.next  # tupla de próximos nós; vazia = terminou
        if "deploy" in nxt:
            # Pausou no gate HITL. Persiste entry + diff para o painel de aprovação.
            entry = snap.values.get("atlas_entry") or {}
            run.payload["atlas_entry"] = entry
            run.payload["branch"] = f"{run.slug}/objeto-educacional"
            run.payload["diff"] = (
                f"+ {run.slug}/index.html\n+ {run.slug}/README.md\n"
                f"+ {run.slug}/{run.slug}.png\n"
                f"~ index.html (DATA += {run.slug})\n~ README.md (catálogo)")
            run.checklist = snap.values.get("checklist", [])
            await bus.emit(thread_id, "deploy", "wait", "Aguardando aprovação humana.")
            await bus.emit_status(thread_id, RUN_AGUARDANDO)
        else:
            status = snap.values.get("status_final")
            if status == "sucesso":
                run.payload["pr_url"] = snap.values.get("pr_url")
                run.payload["branch"] = snap.values.get("branch")
                await bus.emit_status(thread_id, RUN_CONCLUIDO)
            else:
                await bus.emit_status(thread_id, RUN_FALHA)
    except Exception as exc:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        if run:
            await bus.emit(thread_id, "_run", "fail", f"Erro: {exc}")
            await bus.emit_status(thread_id, RUN_FALHA)


def start_run(tema: str, metafora: str, slug: str, max_tentativas: int, hitl: bool) -> str:
    thread_id = slug  # 1 thread por objeto (slug determinístico)
    run = Run(thread_id, tema, metafora, slug, max_tentativas, hitl)
    bus.create_run(run)

    initial = {
        "tema": tema, "metafora": metafora, "slug": slug,
        "n_conceitos": 12, "max_tentativas": max_tentativas, "hitl": hitl,
        "tentativas_imagem": 0, "tentativas_correcao": 0,
        "erros_validacao": [], "validacao_ok": False, "status_final": "",
    }
    asyncio.create_task(_drive(thread_id, initial))
    return thread_id


async def approve_run(thread_id: str) -> None:
    run = bus.get(thread_id)
    if not run:
        raise KeyError(thread_id)
    await bus.emit_status(thread_id, RUN_EM_EXEC)
    await _drive(thread_id, None)  # retoma → executa deploy → END


async def reject_run(thread_id: str) -> None:
    run = bus.get(thread_id)
    if not run:
        raise KeyError(thread_id)
    await bus.emit(thread_id, "deploy", "skip", "Descartado pelo usuário.")
    await bus.emit_status(thread_id, RUN_FALHA)


async def regenerate_run(thread_id: str) -> None:
    """Força nova tentativa do objeto a partir do estado atual."""
    run = bus.get(thread_id)
    if not run:
        raise KeyError(thread_id)
    config = _config(thread_id)
    graph = await get_graph()
    await graph.aupdate_state(config, {"validacao_ok": False,
                                       "erros_validacao": ["Regeneração solicitada pelo usuário."]},
                              as_node="validar_objeto")
    await bus.emit_status(thread_id, RUN_EM_EXEC)
    asyncio.create_task(_drive(thread_id, None))
