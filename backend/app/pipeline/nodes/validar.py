"""Nó 4 — validar_objeto: Playwright conta [data-conceito] em #figura (A3).

Fase 1: stub monta o checklist §4.4 e, para DEMONSTRAR o loop de autocorreção,
falha na 1ª tentativa e passa na 2ª. Fase 4 liga o Playwright real.
"""
from __future__ import annotations

import asyncio

from ..state import PipelineState
from ._util import emit

CHECK_LABELS = [
    "Abre sem erro no console",
    "12 hotspots ([data-conceito] em #figura)",
    "Cada estação abre o modal",
    "Tour guiado percorre todos",
    "Teclado: Tab/Enter/Esc/setas",
    "Sem requisições externas (sem CDN)",
    ":focus-visible presente",
    "prefers-reduced-motion respeitado",
]


async def validar_objeto(state: PipelineState, config) -> dict:
    await emit(config, "validar_objeto", "running", "Validando o objeto (§4.4)…")
    await asyncio.sleep(0.5)  # stub

    tentativa = state.get("tentativas_correcao", 0)
    # Fase 1: simula 1 falha para exercitar o loop validar→gerar_objeto.
    falhar = tentativa == 0
    erros = (["3 estações sem aria-label", "imagem não carregou"] if falhar else [])
    checklist = [{"label": lbl, "ok": (not falhar) or i not in (1, 5)}
                 for i, lbl in enumerate(CHECK_LABELS)]

    if falhar:
        await emit(config, "validar_objeto", "fail",
                   "Validação falhou: " + "; ".join(erros) + " → reinjetando no gerar_objeto.",
                   {"erros": erros})
    else:
        await emit(config, "validar_objeto", "ok", "Validação OK (8/8).", {"erros": []})

    return {
        "validacao_ok": not falhar,
        "erros_validacao": erros,
        "checklist": checklist,
        "tentativas_correcao": tentativa + 1,
    }
