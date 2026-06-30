"""Estado global do grafo LangGraph + utilidades de slug."""
from __future__ import annotations

import re
import unicodedata
from typing import List, Optional, TypedDict


class PipelineState(TypedDict, total=False):
    # Entrada do usuário
    tema: str
    metafora: str
    slug: str
    n_conceitos: int
    max_tentativas: int
    hitl: bool

    # Etapas 1 e 2 (imagem)
    prompt_imagem: Optional[str]
    caminho_imagem: Optional[str]
    tentativas_imagem: int

    # Etapa 3 (objeto)
    objeto_json: Optional[dict]   # JSON emitido pela LLM (conceitos/GEO/ORDEM/RELACOES/metadados)
    html_path: Optional[str]
    readme_path: Optional[str]

    # Etapa 4 (validação)
    erros_validacao: List[str]
    validacao_ok: bool
    tentativas_correcao: int
    checklist: List[dict]         # itens {label, ok} para a tela Console

    # Etapas 5 e 6 (atlas + deploy)
    atlas_entry: Optional[dict]
    branch: Optional[str]
    pr_url: Optional[str]
    status_final: str             # "" | "sucesso" | "falha"


def slugify(tema: str, metafora: str) -> str:
    """Deriva o slug determinístico: {tema}-{metafora} em kebab-case, sem acento."""
    raw = f"{tema}-{metafora}".strip().lower()
    # remove acentos
    raw = unicodedata.normalize("NFKD", raw)
    raw = "".join(ch for ch in raw if not unicodedata.combining(ch))
    # tudo que não é [a-z0-9] vira hífen
    raw = re.sub(r"[^a-z0-9]+", "-", raw)
    return raw.strip("-")
