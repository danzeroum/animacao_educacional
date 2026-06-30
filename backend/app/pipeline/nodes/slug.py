"""Nó 0 — definir_slug: deriva o slug determinístico e prepara a pasta do objeto."""
from __future__ import annotations

from ...config import settings
from ..state import PipelineState, slugify
from ._util import emit


async def definir_slug(state: PipelineState, config) -> dict:
    await emit(config, "definir_slug", "running", "Derivando slug…")

    slug = slugify(state["tema"], state["metafora"])
    pasta = settings().repo_root / slug
    sobrescrita = pasta.exists()
    pasta.mkdir(parents=True, exist_ok=True)

    msg = f"slug = {slug}" + (" (pasta já existia — sobrescrevendo)" if sobrescrita else "")
    await emit(config, "definir_slug", "ok", msg, {"slug": slug})

    return {
        "slug": slug,
        "n_conceitos": state.get("n_conceitos", 12),
        "tentativas_imagem": 0,
        "tentativas_correcao": 0,
        "erros_validacao": [],
        "validacao_ok": False,
        "status_final": "",
    }
