"""Configuração central da Forja (lê do ambiente / .env)."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# backend/app/config.py -> backend/app -> backend -> repo root
_DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[2]


@lru_cache
def settings() -> "Settings":
    return Settings()


class Settings:
    def __init__(self) -> None:
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.deepseek_base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.gemini_image_model = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")

        repo = os.getenv("REPO_ROOT", "").strip()
        self.repo_root = Path(repo).resolve() if repo else _DEFAULT_REPO_ROOT

        self.max_tentativas = int(os.getenv("FORJA_MAX_TENTATIVAS", "3"))
        self.db_path = os.getenv("FORJA_DB", "./forja.db")

        self.github_repo = os.getenv("GITHUB_REPO", "danzeroum/animacao_educacional")
        self.github_base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        # dry-run: NÃO faz git mutável nem abre PR (default seguro; produção local = "false")
        self.dry_run = os.getenv("FORJA_DRY_RUN", "true").lower() not in ("0", "false", "no")

    @property
    def template_path(self) -> Path:
        return Path(__file__).resolve().parent / "pipeline" / "templates" / "objeto.template.html"

    @property
    def has_deepseek(self) -> bool:
        return bool(self.deepseek_api_key)

    @property
    def has_gemini(self) -> bool:
        return bool(self.gemini_api_key)

    @property
    def has_github_token(self) -> bool:
        return bool(self.github_token)
