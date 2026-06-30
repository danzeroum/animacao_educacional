"""Rotas de catálogo/admin: objetos, pull requests, config, providers."""
from __future__ import annotations

import re

from fastapi import APIRouter

from ..config import settings
from ..events import bus

router = APIRouter()

# objetos = pastas na raiz com index.html (exclui pastas de infra)
_IGNORAR = {"backend", "frontend", "docs", "node_modules", ".git"}


@router.get("/objects")
async def objetos():
    root = settings().repo_root
    itens = []
    atlas = (root / "index.html").read_text(encoding="utf-8") if (root / "index.html").exists() else ""
    linkados = set(re.findall(r"id:'([^']+)'", atlas))
    for d in sorted(p for p in root.iterdir() if p.is_dir() and p.name not in _IGNORAR):
        if not (d / "index.html").exists():
            continue
        slug = d.name
        tem_img = (d / f"{slug}.png").exists()
        itens.append({
            "slug": slug,
            "tem_imagem": tem_img,
            "no_atlas": slug in linkados,
            "status": "No Atlas" if slug in linkados else "Aguardando",
        })
    return {"objetos": itens, "total": len(itens),
            "linkados": sum(1 for i in itens if i["no_atlas"])}


@router.get("/pulls")
async def pull_requests():
    pulls = []
    for r in bus.runs.values():
        pr = r.payload.get("pr_url")
        if pr:
            pulls.append({"slug": r.slug, "branch": r.payload.get("branch"),
                          "url": pr, "status": "Aberto"})
    return {"pulls": pulls}


@router.get("/providers")
async def providers():
    s = settings()
    return {
        "deepseek": {"model": s.deepseek_model, "base_url": s.deepseek_base_url,
                     "configurado": s.has_deepseek, "grant_usado": 2.9, "grant_total": 5.0},
        "gemini": {"model": s.gemini_image_model, "configurado": s.has_gemini,
                   "imagens_hoje": 0, "cota_diaria": 500},
        "github": {"repo": s.github_repo, "base": s.github_base_branch,
                   "acao": "create_pull_request (MCP)"},
    }


@router.get("/config")
async def config():
    s = settings()
    return {
        "servidor": "localhost:8000",
        "eventos": "SSE · /runs/{id}/stream",
        "checkpointer": f"SqliteSaver · {s.db_path}",
        "aprovacao_humana": "ATIVO",
        "max_tentativas": s.max_tentativas,
        "padrao_branch": "{slug}/objeto-educacional",
        "repo_root": str(s.repo_root),
    }
