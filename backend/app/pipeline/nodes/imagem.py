"""Nó 2 — gerar_imagem: Gemini 2.5 Flash Image (Fase 1: stub grava PNG placeholder).

Fase 2 liga o Gemini real (generate_content + inline_data.data) com retry e
guardrail de cota.
"""
from __future__ import annotations

import asyncio
import struct
import zlib

from ...config import settings
from ..state import PipelineState
from ._util import emit


def _png_placeholder(path) -> None:
    """Gera um PNG 16x9 cinza sólido sem dependências externas (Fase 1)."""
    w, h = 16, 9
    raw = b"".join(b"\x00" + b"\x4a\x3a\x2a" * w for _ in range(h))  # filtro 0 + pixels RGB

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)  # 8-bit RGB
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
    path.write_bytes(png)


async def gerar_imagem(state: PipelineState, config) -> dict:
    await emit(config, "gerar_imagem", "running", "Gerando imagem de fundo (Gemini)…")
    await asyncio.sleep(0.5)  # stub

    slug = state["slug"]
    destino = settings().repo_root / slug / f"{slug}.png"
    _png_placeholder(destino)

    await emit(config, "gerar_imagem", "ok", f"Imagem salva: {slug}.png (placeholder)",
               {"caminho_imagem": str(destino)})
    return {
        "caminho_imagem": str(destino),
        "tentativas_imagem": state.get("tentativas_imagem", 0) + 1,
    }
