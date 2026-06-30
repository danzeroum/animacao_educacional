"""Nó 5 — atualizar_atlas: insere a entrada por marcadores-sentinela (correção A2).

- index.html raiz: nova entrada do array `DATA` antes de `/* __ATLAS_ENTRIES__ */`.
- README.md raiz: linha do catálogo antes de `<!-- __CATALOGO__ -->`.
Idempotente: se o slug já estiver no Atlas, não duplica.
"""
from __future__ import annotations

import json

from ...config import settings
from ..state import PipelineState
from ._util import emit

ATLAS_MARK = "/* __ATLAS_ENTRIES__ */"
CAT_MARK = "<!-- __CATALOGO__ -->"


def _entry_js(entry: dict) -> str:
    """Serializa a entrada no estilo do array DATA (chaves sem aspas, aspas simples)."""
    def val(v):
        if isinstance(v, list):
            return "[" + ",".join("'" + str(x).replace("'", "\\'") + "'" for x in v) + "]"
        if isinstance(v, (int, float)):
            return str(v)
        return "'" + str(v).replace("'", "\\'") + "'"

    campos = ["id", "nome", "tema", "cenario", "icone", "cor", "n", "cat", "nivel", "tags", "desc"]
    corpo = ", ".join(f"{k}:{val(entry[k])}" for k in campos if k in entry)
    return "    { " + corpo + " },"


def _linha_catalogo(entry: dict, slug: str) -> str:
    nome, tema, cen = entry.get("nome", slug), entry.get("tema", ""), entry.get("cenario", "")
    return f"| {nome} | {tema} | {cen} | Devs juniores | [`{slug}/`](./{slug}/) |"


async def atualizar_atlas(state: PipelineState, config) -> dict:
    await emit(config, "atualizar_atlas", "running", "Atualizando Atlas e catálogo…")
    root = settings().repo_root
    slug = state["slug"]
    meta = (state.get("objeto_json") or {}).get("metadados", {})
    n = state.get("n_conceitos", 12)

    entry = {
        "id": slug, "nome": meta.get("titulo", slug), "tema": meta.get("tema") or meta.get("titulo", ""),
        "cenario": meta.get("cenario", ""), "icone": meta.get("icone", "🪨"),
        "cor": meta.get("cor", "#d9a441"), "n": n, "cat": meta.get("cat", "arq"),
        "nivel": meta.get("nivel", "Iniciante"), "tags": meta.get("tags", []),
        "desc": meta.get("desc", ""),
    }

    idx = root / "index.html"
    readme = root / "README.md"
    mudou = []
    ja_existe = False

    # --- Atlas (index.html) ---
    html = idx.read_text(encoding="utf-8")
    if f"id:'{slug}'" in html or f'id:"{slug}"' in html:
        ja_existe = True
    elif ATLAS_MARK in html:
        html = html.replace(ATLAS_MARK, _entry_js(entry) + "\n    " + ATLAS_MARK, 1)
        idx.write_text(html, encoding="utf-8")
        mudou.append("index.html")
    else:
        await emit(config, "atualizar_atlas", "fail", f"Marcador {ATLAS_MARK} ausente no index.html raiz.")
        raise RuntimeError("marcador-sentinela do Atlas ausente")

    # --- Catálogo (README.md) ---
    rd = readme.read_text(encoding="utf-8")
    if f"](./{slug}/)" in rd:
        ja_existe = ja_existe or True
    elif CAT_MARK in rd:
        rd = rd.replace(CAT_MARK, _linha_catalogo(entry, slug) + "\n" + CAT_MARK, 1)
        readme.write_text(rd, encoding="utf-8")
        mudou.append("README.md")
    else:
        await emit(config, "atualizar_atlas", "fail", f"Marcador {CAT_MARK} ausente no README.md raiz.")
        raise RuntimeError("marcador-sentinela do catálogo ausente")

    diff = (f"+ {slug}/index.html\n+ {slug}/README.md\n+ {slug}/{slug}.png\n"
            + "\n".join(f"~ {m}" for m in mudou))
    msg = ("Atlas já continha o slug (idempotente)." if ja_existe and not mudou
           else f"Atlas e catálogo atualizados ({', '.join(mudou)}).")
    await emit(config, "atualizar_atlas", "ok", msg, {"atlas_entry": entry, "diff": diff})
    return {"atlas_entry": entry}
