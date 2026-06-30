"""Nó 5 — atualizar_atlas: insere a entrada por marcadores-sentinela (A2).

Fase 1: stub apenas prepara a entrada e os diffs. Fase 5 escreve de fato antes
de `/* __ATLAS_ENTRIES__ */` (index.html raiz) e `<!-- __CATALOGO__ -->` (README raiz).
"""
from __future__ import annotations

import asyncio

from ..state import PipelineState
from ._util import emit


async def atualizar_atlas(state: PipelineState, config) -> dict:
    await emit(config, "atualizar_atlas", "running", "Atualizando Atlas e catálogo…")
    await asyncio.sleep(0.4)  # stub

    meta = (state.get("objeto_json") or {}).get("metadados", {})
    entry = {
        "id": state["slug"], "nome": meta.get("titulo", state["slug"]),
        "tema": meta.get("titulo", ""), "cenario": meta.get("cenario", ""),
        "icone": meta.get("icone", "🪨"), "cor": meta.get("cor", "#d9a441"),
        "n": state.get("n_conceitos", 12), "cat": meta.get("cat", "arq"),
        "nivel": meta.get("nivel", "Iniciante"), "tags": meta.get("tags", []),
        "desc": meta.get("desc", ""),
    }
    diff = (f"+ {state['slug']}/index.html\n+ {state['slug']}/README.md\n"
            f"+ {state['slug']}/{state['slug']}.png\n"
            f"~ index.html (DATA += {state['slug']})\n~ README.md (catálogo)")

    await emit(config, "atualizar_atlas", "ok", "Entrada do Atlas preparada (stub).",
               {"atlas_entry": entry, "diff": diff})
    return {"atlas_entry": entry}
