"""Nó 1 — gerar_prompt: prompt da imagem via DeepSeek (Fase 1: stub).

Fase 2 liga o DeepSeek real (clients.deepseek + prompts.CONTRATO_IMAGEM).
"""
from __future__ import annotations

import asyncio

from ..state import PipelineState
from ._util import emit


async def gerar_prompt(state: PipelineState, config) -> dict:
    await emit(config, "gerar_prompt", "running", "Gerando prompt da imagem (DeepSeek)…")
    await asyncio.sleep(0.4)  # stub: simula latência da API

    prompt = (
        f"[STUB] Ilustração 16:9 da metáfora '{state['metafora']}' para o tema "
        f"'{state['tema']}': 5 nichos em cima, 7 embaixo, separados por pilares, sem texto."
    )
    await emit(config, "gerar_prompt", "ok", "Prompt pronto.", {"prompt_imagem": prompt})
    return {"prompt_imagem": prompt}
