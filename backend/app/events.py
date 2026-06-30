"""Barramento de eventos por thread_id (alimenta o SSE) + registro de runs em memória.

Cada nó publica `{node, status, payload, ts}`. A tela Console consome via SSE.
O histórico é mantido para que um assinante tardio receba os eventos anteriores.
"""
from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, List, Optional

# Ordem canônica dos 7 nós exibidos na trilha do grafo (frontend).
NODES = [
    "definir_slug",
    "gerar_prompt",
    "gerar_imagem",
    "gerar_objeto",
    "validar_objeto",
    "atualizar_atlas",
    "deploy",
]

# Status de um nó (enum do handoff B0).
NODE_STATUS = {"pending", "running", "ok", "fail", "skip", "wait"}
# Status de um run.
RUN_EM_EXEC = "Em execução"
RUN_AGUARDANDO = "Aguardando aprovação"
RUN_CONCLUIDO = "Concluído"
RUN_FALHA = "Falha"


def now_ms() -> int:
    return int(time.time() * 1000)


class Run:
    """Metadados + estado vivo de uma execução (uma thread do grafo)."""

    def __init__(self, thread_id: str, tema: str, metafora: str, slug: str,
                 max_tentativas: int, hitl: bool) -> None:
        self.thread_id = thread_id
        self.tema = tema
        self.metafora = metafora
        self.slug = slug
        self.max_tentativas = max_tentativas
        self.hitl = hitl
        self.status = RUN_EM_EXEC
        self.created_at = now_ms()
        self.tentativas = 0
        self.nodes: Dict[str, str] = {n: "pending" for n in NODES}
        self.log: List[dict] = []
        self.checklist: List[dict] = []
        self.payload: Dict[str, Any] = {}   # diffs, pr_url, atlas_entry, erros...

    def to_summary(self) -> dict:
        return {
            "thread_id": self.thread_id,
            "tema": self.tema,
            "metafora": self.metafora,
            "slug": self.slug,
            "status": self.status,
            "tentativas": self.tentativas,
            "max_tentativas": self.max_tentativas,
            "created_at": self.created_at,
        }

    def to_detail(self) -> dict:
        return {
            **self.to_summary(),
            "hitl": self.hitl,
            "nodes": self.nodes,
            "log": self.log,
            "checklist": self.checklist,
            "payload": self.payload,
        }


class EventBus:
    def __init__(self) -> None:
        self.runs: Dict[str, Run] = {}
        self._queues: Dict[str, List[asyncio.Queue]] = {}
        self._history: Dict[str, List[dict]] = {}

    # --- runs ---
    def create_run(self, run: Run) -> None:
        self.runs[run.thread_id] = run
        self._history[run.thread_id] = []
        self._queues.setdefault(run.thread_id, [])

    def get(self, thread_id: str) -> Optional[Run]:
        return self.runs.get(thread_id)

    def list(self) -> List[dict]:
        return [r.to_summary() for r in sorted(
            self.runs.values(), key=lambda r: r.created_at, reverse=True)]

    # --- pub/sub ---
    async def emit(self, thread_id: str, node: str, status: str,
                   message: str = "", payload: Optional[dict] = None) -> None:
        run = self.runs.get(thread_id)
        if run and node in run.nodes and status in NODE_STATUS:
            run.nodes[node] = status
        ev = {"node": node, "status": status, "message": message,
              "payload": payload or {}, "ts": now_ms()}
        if run is not None and message:
            run.log.append({"ts": ev["ts"], "status": status, "message": message})
        self._history.setdefault(thread_id, []).append(ev)
        for q in list(self._queues.get(thread_id, [])):
            await q.put(ev)

    async def emit_status(self, thread_id: str, run_status: str) -> None:
        run = self.runs.get(thread_id)
        if run:
            run.status = run_status
        await self.emit(thread_id, "_run", run_status, message=f"status: {run_status}")

    def subscribe(self, thread_id: str) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        # replay do histórico para assinantes tardios
        for ev in self._history.get(thread_id, []):
            q.put_nowait(ev)
        self._queues.setdefault(thread_id, []).append(q)
        return q

    def unsubscribe(self, thread_id: str, q: asyncio.Queue) -> None:
        if thread_id in self._queues and q in self._queues[thread_id]:
            self._queues[thread_id].remove(q)


# instância global do processo
bus = EventBus()
