"""Nó 3 — gerar_objeto: DeepSeek emite JSON; Python injeta no template fixo (A1).

Fase 1: stub produz um objeto_json mínimo e injeta no template para validar a
mecânica de injeção. Fase 3 liga o DeepSeek real + validação de schema.
"""
from __future__ import annotations

import json

from ...config import settings
from .. import clients
from ..prompts import CORRECAO_SUFIXO, OBJETO_JSON
from ..render import render_objeto, validar_schema
from ..state import PipelineState
from ..util import QuotaError, with_retry
from ._util import emit


def _parse_json(texto: str) -> dict:
    """Extrai JSON do texto da LLM, tolerando cercas ```json … ```."""
    t = texto.strip()
    if t.startswith("```"):
        t = t.split("```", 2)[1] if t.count("```") >= 2 else t.strip("`")
        if t.lstrip().startswith("json"):
            t = t.lstrip()[4:]
    i, j = t.find("{"), t.rfind("}")
    if i != -1 and j != -1:
        t = t[i:j + 1]
    return json.loads(t)


def _chamar_deepseek(state: PipelineState) -> dict:
    s = settings()
    prompt = OBJETO_JSON.format(tema=state["tema"], metafora=state["metafora"],
                                n=state.get("n_conceitos", 12))
    erros = state.get("erros_validacao") or []
    if erros:
        prompt += CORRECAO_SUFIXO.format(erros="\n".join(f"- {e}" for e in erros))

    resp = clients.deepseek().chat.completions.create(
        model=s.deepseek_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=8000,
        response_format={"type": "json_object"},
    )
    objeto = _parse_json(resp.choices[0].message.content or "")
    problemas = validar_schema(objeto, state.get("n_conceitos", 12))
    if problemas:
        # schema inválido → força nova tentativa da própria LLM (não é cota)
        raise ValueError("JSON fora do schema: " + "; ".join(problemas[:6]))
    return objeto


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

    if not settings().has_deepseek:
        objeto = _stub_objeto(state)
        await emit(config, "gerar_objeto", "running", "(stub — sem DEEPSEEK_API_KEY)")
    else:
        async def _aviso(i, exc):
            await emit(config, "gerar_objeto", "running", f"Tentativa {i} do JSON falhou ({exc}); repetindo…")
        try:
            objeto = await with_retry(lambda: _chamar_deepseek(state), on_retry=_aviso)
        except QuotaError as e:
            await emit(config, "gerar_objeto", "fail", f"Cota da DeepSeek esgotada: {e}")
            raise
        except Exception as e:  # noqa: BLE001
            await emit(config, "gerar_objeto", "fail", f"JSON inválido após retries: {e}")
            raise

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
