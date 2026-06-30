"""Nó 6 — deploy: roda APÓS aprovação humana (interrupt_before=["deploy"]).

Fase 1: stub marca sucesso e simula um PR. Fase 5 faz git branch/commit/push e
abre o PR via GitHub MCP.
"""
from __future__ import annotations

import asyncio

from ...config import settings
from ..state import PipelineState
from ._util import emit


async def deploy(state: PipelineState, config) -> dict:
    await emit(config, "deploy", "running", "Aprovado — abrindo Pull Request…")
    await asyncio.sleep(0.5)  # stub

    branch = f"{state['slug']}/objeto-educacional"
    pr_url = f"https://github.com/{settings().github_repo}/pull/NEW"  # stub

    await emit(config, "deploy", "ok", f"PR aberto: {branch} → {settings().github_base_branch}",
               {"branch": branch, "pr_url": pr_url})
    return {"branch": branch, "pr_url": pr_url, "status_final": "sucesso"}


async def notificar_falha(state: PipelineState, config) -> dict:
    erros = state.get("erros_validacao", [])
    await emit(config, "deploy", "skip",
               f"Falha após {state.get('tentativas_correcao', 0)} tentativas. Deploy cancelado.",
               {"erros": erros})
    return {"status_final": "falha"}
