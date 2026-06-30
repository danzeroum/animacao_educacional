"""Nó 2 — gerar_imagem: imagem de fundo via Gemini 2.5 Flash Image.

Real quando há GEMINI_API_KEY; senão, grava um PNG placeholder (offline).
Trata retry + guardrail de cota.
"""
from __future__ import annotations

import struct
import zlib
from io import BytesIO
from pathlib import Path

from ...config import settings
from .. import clients
from ..state import PipelineState
from ..util import QuotaError, with_retry
from ._util import emit


def _png_placeholder(path: Path) -> None:
    """PNG 16x9 cinza sólido, sem dependências (fallback offline)."""
    w, h = 16, 9
    raw = b"".join(b"\x00" + b"\x4a\x3a\x2a" * w for _ in range(h))

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
    path.write_bytes(png)


def _extrair_bytes(resp) -> bytes | None:
    """Pega os bytes da primeira parte com inline_data (imagem) da resposta."""
    for cand in getattr(resp, "candidates", None) or []:
        content = getattr(cand, "content", None)
        for part in getattr(content, "parts", None) or []:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                return inline.data
    return None


def _chamar_gemini(prompt: str, destino: Path) -> None:
    s = settings()
    resp = clients.gemini().models.generate_content(
        model=s.gemini_image_model,
        contents=[prompt],
    )
    data = _extrair_bytes(resp)
    if not data:
        # sem imagem (ex.: bloqueio de segurança) → erro transitório p/ retry
        raise RuntimeError("Gemini não retornou imagem (resposta sem inline_data).")
    try:
        from PIL import Image
        Image.open(BytesIO(data)).convert("RGB").save(destino, format="PNG")
    except Exception:  # noqa: BLE001 — se já vier PNG, grava direto
        destino.write_bytes(data)


async def gerar_imagem(state: PipelineState, config) -> dict:
    await emit(config, "gerar_imagem", "running", "Gerando imagem de fundo (Gemini)…")
    slug = state["slug"]
    destino = settings().repo_root / slug / f"{slug}.png"
    destino.parent.mkdir(parents=True, exist_ok=True)
    prompt = state.get("prompt_imagem") or f"Ilustração mapa-metáfora para {slug}."

    if not settings().has_gemini:
        _png_placeholder(destino)
        await emit(config, "gerar_imagem", "ok",
                   f"Imagem salva: {slug}.png (placeholder — sem GEMINI_API_KEY).",
                   {"caminho_imagem": str(destino)})
        return {"caminho_imagem": str(destino),
                "tentativas_imagem": state.get("tentativas_imagem", 0) + 1}

    async def _aviso(i, exc):
        await emit(config, "gerar_imagem", "running", f"Tentativa {i} falhou ({exc}); repetindo…")

    try:
        await with_retry(lambda: _chamar_gemini(prompt, destino), on_retry=_aviso)
    except QuotaError:
        # Imagem é DEGRADÁVEL: cota esgotada não derruba o run — grava placeholder
        # e segue (o resto do pipeline produz o objeto; troque {slug}.png depois).
        _png_placeholder(destino)
        await emit(config, "gerar_imagem", "ok",
                   f"Cota do Gemini esgotada — usei placeholder. Troque {slug}.png depois "
                   "(ou habilite billing no projeto Gemini).",
                   {"caminho_imagem": str(destino), "placeholder": True})
        return {"caminho_imagem": str(destino),
                "tentativas_imagem": state.get("tentativas_imagem", 0) + 1}
    except Exception as e:  # noqa: BLE001
        await emit(config, "gerar_imagem", "fail", f"Falha no Gemini: {e}")
        raise

    await emit(config, "gerar_imagem", "ok", f"Imagem salva: {slug}.png",
               {"caminho_imagem": str(destino)})
    return {"caminho_imagem": str(destino),
            "tentativas_imagem": state.get("tentativas_imagem", 0) + 1}
