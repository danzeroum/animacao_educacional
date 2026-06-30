"""Injeção do objeto_json no template fixo (correção A1).

A LLM emite apenas JSON; aqui montamos o index.html determinístico substituindo
os placeholders do template `objeto.template.html` e geramos o README.md.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

from ..config import settings


def _js(value) -> str:
    """Serializa para JS embutível (JSON é subconjunto de JS; mantém acentos)."""
    return json.dumps(value, ensure_ascii=False, indent=2)


def montar_html(slug: str, objeto: dict) -> str:
    meta = objeto["metadados"]
    n = len(objeto["ordem"])
    tpl = settings().template_path.read_text(encoding="utf-8")

    subst = {
        "{{SLUG}}": slug,
        "{{N}}": str(n),
        "{{TITULO}}": meta["titulo"],
        "{{TITULO_PAGINA}}": meta["titulo_pagina"],
        "{{DESCRICAO}}": meta["descricao"],
        "{{OG_DESC}}": meta["og_desc"],
        "{{TESE}}": meta["tese"],
        "{{FIGURA_DICA}}": meta["figura_dica"],
        "{{IMG_ALT}}": meta["img_alt"],
        "{{DICA_LABEL}}": meta["dica_label"],
        "{{RODAPE}}": meta["rodape"],
        "{{ICONE}}": meta["icone"],
        "{{TEMA}}": meta.get("titulo", slug),
        "{{CONCEITOS_JSON}}": _js(objeto["conceitos"]),
        "{{GEO_JSON}}": _js(objeto["geo"]),
        "{{ORDEM_JSON}}": _js(objeto["ordem"]),
        "{{RELACOES_JSON}}": _js(objeto["relacoes"]),
    }
    html = tpl
    for k, v in subst.items():
        html = html.replace(k, v)
    return html


def montar_readme(slug: str, objeto: dict) -> str:
    meta = objeto["metadados"]
    linhas = [
        f"# {meta['titulo']} — {meta['cenario']}",
        "",
        meta["descricao"],
        "",
        "## Como usar",
        "",
        f"Abra o arquivo `index.html` diretamente no seu navegador. "
        f"A imagem `{slug}.png` deve estar na mesma pasta.",
        "",
        "## Mapeamento",
        "",
        "| Elemento da metáfora | Conceito técnico |",
        "|---|---|",
    ]
    for cid in objeto["ordem"]:
        c = objeto["conceitos"][cid]
        elemento = c["titulo"].split("—")[-1].strip() if "—" in c["titulo"] else c["label"]
        conceito = c["titulo"].split("—")[0].strip() if "—" in c["titulo"] else c["label"]
        linhas.append(f"| {elemento} | {conceito} |")
    return "\n".join(linhas) + "\n"


def render_objeto(slug: str, objeto: dict, repo_root: Path) -> Tuple[Path, Path]:
    pasta = repo_root / slug
    pasta.mkdir(parents=True, exist_ok=True)
    html_path = pasta / "index.html"
    readme_path = pasta / "README.md"
    html_path.write_text(montar_html(slug, objeto), encoding="utf-8")
    readme_path.write_text(montar_readme(slug, objeto), encoding="utf-8")
    return html_path, readme_path
