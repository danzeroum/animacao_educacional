"""Nó 1 — gerar_prompt: prompt da imagem via DeepSeek.

Real quando há DEEPSEEK_API_KEY; senão, fallback stub (pipeline roda offline).
"""
from __future__ import annotations

from ...config import settings
from .. import clients
from ..prompts import CONTRATO_IMAGEM
from ..state import PipelineState
from ..util import QuotaError, with_retry
from ._util import emit

_STUB = ("[STUB] Ilustração 16:9 da metáfora '{metafora}' para o tema '{tema}': "
         "5 nichos em cima, 7 embaixo, separados por pilares, sem texto.")


def _chamar_deepseek(tema: str, metafora: str) -> str:
    s = settings()
    resp = clients.deepseek().chat.completions.create(
        model=s.deepseek_model,
        messages=[{"role": "user",
                   "content": CONTRATO_IMAGEM.format(tema=tema, metafora=metafora)}],
        temperature=0.8,
        max_tokens=600,
    )
    return (resp.choices[0].message.content or "").strip()


async def gerar_prompt(state: PipelineState, config) -> dict:
    await emit(config, "gerar_prompt", "running", "Gerando prompt da imagem (DeepSeek)…")
    tema, metafora = state["tema"], state["metafora"]

    if not settings().has_deepseek:
        prompt = _STUB.format(tema=tema, metafora=metafora)
        await emit(config, "gerar_prompt", "ok",
                   "Prompt pronto (stub — sem DEEPSEEK_API_KEY).", {"prompt_imagem": prompt})
        return {"prompt_imagem": prompt}

    async def _aviso(i, exc):
        await emit(config, "gerar_prompt", "running", f"Tentativa {i} falhou ({exc}); repetindo…")

    try:
        prompt = await with_retry(lambda: _chamar_deepseek(tema, metafora), on_retry=_aviso)
    except QuotaError as e:
        await emit(config, "gerar_prompt", "fail", f"Cota da DeepSeek esgotada: {e}")
        raise
    except Exception as e:  # noqa: BLE001
        await emit(config, "gerar_prompt", "fail", f"Falha no DeepSeek: {e}")
        raise

    await emit(config, "gerar_prompt", "ok", "Prompt pronto.", {"prompt_imagem": prompt})
    return {"prompt_imagem": prompt}
