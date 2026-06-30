"""Nó 3 — gerar_objeto: DeepSeek emite JSON; Python injeta no template fixo (A1).

Fase 1: stub produz um objeto_json mínimo e injeta no template para validar a
mecânica de injeção. Fase 3 liga o DeepSeek real + validação de schema.
"""
from __future__ import annotations

import asyncio
import json

from ...config import settings
from ..state import PipelineState
from ._util import emit
from ..render import render_objeto


def _stub_objeto(state: PipelineState) -> dict:
    """Objeto_json mínimo (N conceitos) só para exercitar a injeção no template."""
    n = state.get("n_conceitos", 12)
    ordem, conceitos, geo, relacoes = [], {}, {}, {}
    for i in range(n):
        cid = f"conceito_{i+1}"
        ordem.append(cid)
        topo = i < 5
        col = i if topo else i - 5
        left = (col * 18 + 2) if topo else (col * 13 + 2)
        top = 8 if topo else 60
        conceitos[cid] = {
            "zona": "Faixa superior" if topo else "Faixa inferior",
            "titulo": f"Conceito {i+1} — Elemento {i+1}",
            "icone": "🪨", "cor": "#d9a441", "label": f"Conceito {i+1}",
            "metafora": f"[STUB] liga o elemento {i+1} da metáfora ao conceito {i+1}.",
            "bullets": ["[stub] bullet 1", "[stub] bullet 2", "[stub] bullet 3"],
            "ferramentas": [{"nome": "Exemplo", "url": "https://example.com"}],
            "dica": "[stub] dica prática.",
        }
        geo[cid] = [left, top, 14, 30]
        relacoes[cid] = {"ids": [ordem[i - 1]] if i else [], "nota": "[stub] conexão."}
    return {
        "metadados": {
            "titulo": f"{state['tema'].title()}",
            "titulo_pagina": f"{state['tema'].title()} — {state['metafora'].title()}",
            "descricao": "[stub] objeto educacional.",
            "og_desc": "[stub] clique nos nichos para aprender.",
            "tese": "[stub] a figura ensina por inteiro.",
            "figura_dica": "Clique em qualquer nicho.",
            "img_alt": "[stub] ilustração de fundo.",
            "dica_label": "Dica", "rodape": "[stub] frase de rodapé.",
            "icone": "🪨", "cenario": state["metafora"].title(), "cor": "#d9a441",
            "cat": "arq", "nivel": "Iniciante",
            "tags": ["stub1", "stub2", "stub3"], "desc": "[stub] uma linha.",
        },
        "ordem": ordem, "conceitos": conceitos, "geo": geo, "relacoes": relacoes,
    }


async def gerar_objeto(state: PipelineState, config) -> dict:
    tentativa = state.get("tentativas_correcao", 0) + 1
    await emit(config, "gerar_objeto", "running",
               f"Gerando objeto (JSON → template) · tentativa {tentativa}…")
    await asyncio.sleep(0.5)  # stub

    objeto = _stub_objeto(state)
    html_path, readme_path = render_objeto(state["slug"], objeto, settings().repo_root)

    await emit(config, "gerar_objeto", "ok",
               f"index.html + README.md escritos ({len(objeto['ordem'])} conceitos).",
               {"objeto_json": objeto, "html_path": str(html_path)})
    return {
        "objeto_json": objeto,
        "html_path": str(html_path),
        "readme_path": str(readme_path),
        "atlas_entry": {"id": state["slug"], **objeto["metadados"]},
    }
