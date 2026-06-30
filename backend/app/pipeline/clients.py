"""Factories dos provedores. Lazy: só constroem o cliente quando a chave existe."""
from __future__ import annotations

from functools import lru_cache

from ..config import settings


@lru_cache
def deepseek():
    """Cliente OpenAI-compatible apontando para a DeepSeek."""
    from openai import OpenAI

    s = settings()
    if not s.has_deepseek:
        raise RuntimeError("DEEPSEEK_API_KEY ausente — configure o .env.")
    return OpenAI(api_key=s.deepseek_api_key, base_url=s.deepseek_base_url)


@lru_cache
def gemini():
    """Cliente google-genai (Gemini Developer API / AI Studio)."""
    from google import genai

    s = settings()
    if not s.has_gemini:
        raise RuntimeError("GEMINI_API_KEY ausente — configure o .env.")
    return genai.Client(api_key=s.gemini_api_key)
