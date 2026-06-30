"""Nó 2 — gerar_imagem: imagem de fundo do objeto.

Provedor configurável por `IMAGE_PROVIDER`:
- "pollinations" (default): grátis, sem chave/cartão.
- "gemini": Gemini 2.5 Flash Image (exige billing/saldo no projeto).
Sem provedor disponível (ex.: gemini sem chave) → grava um PNG placeholder.
Trata retry + guardrail de cota (cota esgotada → placeholder, não derruba o run).
"""
from __future__ import annotations

import struct
import urllib.parse
import urllib.request
import zlib
from io import BytesIO
from pathlib import Path

from ...config import settings
from .. import clients
from ..state import PipelineState
from ..util import QuotaError, with_retry
from ._util import emit


def _salvar_png(data: bytes, destino: Path) -> None:
    try:
        from PIL import Image
        Image.open(BytesIO(data)).convert("RGB").save(destino, format="PNG")
    except Exception:  # noqa: BLE001 — se já vier PNG, grava direto
        destino.write_bytes(data)


def _chamar_pollinations(prompt: str, destino: Path) -> None:
    """Pollinations.ai — text-to-image grátis e sem chave (GET retorna a imagem)."""
    s = settings()
    params = urllib.parse.urlencode({
        "width": 1280, "height": 720, "nologo": "true",
        "model": s.pollinations_model, "seed": abs(hash(prompt)) % 100000,
    })
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "forja-pipeline"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    if not data:
        raise RuntimeError("Pollinations retornou vazio.")
    _salvar_png(data, destino)


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
    _salvar_png(data, destino)


# provedor → (função, rótulo)
_PROVIDERS = {
    "pollinations": (_chamar_pollinations, "Pollinations"),
    "gemini": (_chamar_gemini, "Gemini"),
}


async def gerar_imagem(state: PipelineState, config) -> dict:
    s = settings()
    provider = s.image_provider if s.image_provider in _PROVIDERS else "pollinations"
    fn, rotulo = _PROVIDERS[provider]
    slug = state["slug"]
    destino = s.repo_root / slug / f"{slug}.png"
    destino.parent.mkdir(parents=True, exist_ok=True)
    prompt = state.get("prompt_imagem") or f"Ilustração mapa-metáfora para {slug}."

    await emit(config, "gerar_imagem", "running", f"Gerando imagem de fundo ({rotulo})…")

    def _placeholder(msg: str) -> dict:
        _png_placeholder(destino)
        return {"caminho_imagem": str(destino),
                "tentativas_imagem": state.get("tentativas_imagem", 0) + 1, "_msg": msg}

    # Sem condição de gerar (gemini sem chave) → placeholder.
    if not s.image_ready:
        out = _placeholder(f"Imagem: placeholder ({rotulo} sem chave). Troque {slug}.png depois.")
        await emit(config, "gerar_imagem", "ok", out.pop("_msg"),
                   {"caminho_imagem": str(destino), "placeholder": True})
        return out

    async def _aviso(i, exc):
        await emit(config, "gerar_imagem", "running", f"Tentativa {i} falhou ({exc}); repetindo…")

    try:
        await with_retry(lambda: fn(prompt, destino), on_retry=_aviso)
    except QuotaError:
        # Imagem é DEGRADÁVEL: cota esgotada não derruba o run — placeholder e segue.
        out = _placeholder(f"Cota do {rotulo} esgotada — usei placeholder. Troque {slug}.png depois.")
        await emit(config, "gerar_imagem", "ok", out.pop("_msg"),
                   {"caminho_imagem": str(destino), "placeholder": True})
        return out
    except Exception as e:  # noqa: BLE001
        # Provedor grátis pode ficar instável; não derruba o run — placeholder + aviso.
        out = _placeholder(f"Falha no {rotulo} ({e}) — usei placeholder. Troque {slug}.png depois.")
        await emit(config, "gerar_imagem", "ok", out.pop("_msg"),
                   {"caminho_imagem": str(destino), "placeholder": True})
        return out

    await emit(config, "gerar_imagem", "ok", f"Imagem salva: {slug}.png ({rotulo}).",
               {"caminho_imagem": str(destino)})
    return {"caminho_imagem": str(destino),
            "tentativas_imagem": state.get("tentativas_imagem", 0) + 1}
