"""Utilidades de resiliência para os nós que chamam APIs externas.

- `QuotaError`: cota/saldo esgotado → o run deve parar com status claro (guardrail).
- `with_retry`: roda uma chamada SÍNCRONA do SDK em thread (não bloqueia o event
  loop), com backoff exponencial. Em erro de cota, falha imediatamente (sem retry).
"""
from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, Optional, TypeVar

T = TypeVar("T")


class QuotaError(Exception):
    """Cota/saldo da API esgotado — não adianta repetir."""


# Sinais de cota/saldo nos provedores (DeepSeek/OpenAI-compatible e Gemini).
_QUOTA_SINAIS = (
    "insufficient balance", "quota", "resource_exhausted", "resourceexhausted",
    "rate limit", "rate_limit", "429", "exceeded your current quota",
    "out of credits", "billing",
)


def _is_quota(exc: Exception) -> bool:
    nome = type(exc).__name__.lower()
    if "ratelimit" in nome or "resourceexhausted" in nome or "quota" in nome:
        return True
    msg = str(exc).lower()
    # status_code, se houver (openai SDK expõe .status_code)
    code = getattr(exc, "status_code", None) or getattr(exc, "code", None)
    if code == 429:
        return True
    return any(s in msg for s in _QUOTA_SINAIS)


async def with_retry(
    fn: Callable[[], T],
    *,
    tentativas: int = 3,
    base: float = 1.0,
    on_retry: Optional[Callable[[int, Exception], Awaitable[None]]] = None,
) -> T:
    """Executa `fn` (síncrona) em thread, com retries e backoff exponencial.

    Lança `QuotaError` imediatamente se o erro for de cota; relança o último
    erro após esgotar as tentativas.
    """
    ultimo: Optional[Exception] = None
    for i in range(1, tentativas + 1):
        try:
            return await asyncio.to_thread(fn)
        except Exception as exc:  # noqa: BLE001
            if _is_quota(exc):
                raise QuotaError(str(exc)) from exc
            ultimo = exc
            if on_retry:
                await on_retry(i, exc)
            if i < tentativas:
                await asyncio.sleep(base * (2 ** (i - 1)))
    assert ultimo is not None
    raise ultimo
