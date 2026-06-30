"""Nó 6 — deploy: roda APÓS aprovação humana (interrupt_before=["deploy"]).

Faz git branch/commit/push do objeto e abre o PR via API REST do GitHub
(GITHUB_TOKEN). Em **dry-run** (default seguro), apenas planeja e mostra o que
seria publicado — não muda o git nem abre PR.
"""
from __future__ import annotations

import asyncio
import json
import subprocess
import urllib.request

from ...config import settings
from ..state import PipelineState
from ._util import emit


def _git(args: list[str], cwd) -> str:
    r = subprocess.run(["git", *args], cwd=str(cwd), check=True,
                       capture_output=True, text=True)
    return r.stdout.strip()


def _commit_msg(slug: str) -> str:
    return f"feat: add {slug} educational object"


def _abrir_pr_rest(slug: str, branch: str) -> str:
    """POST /repos/{owner}/{repo}/pulls com o GITHUB_TOKEN. Retorna a URL do PR."""
    s = settings()
    owner_repo = s.github_repo
    titulo = f"Objeto educacional: {slug.replace('-', ' ')}"
    corpo = (f"Novo objeto mapa-metáfora `{slug}` gerado pela Forja.\n\n"
             f"- `{slug}/index.html`, `{slug}/README.md`, `{slug}/{slug}.png`\n"
             f"- Atlas (`index.html`) e catálogo (`README.md`) atualizados.\n\n"
             "🤖 Generated with [Claude Code](https://claude.com/claude-code)")
    payload = json.dumps({"title": titulo, "head": branch,
                          "base": s.github_base_branch, "body": corpo}).encode()
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner_repo}/pulls",
        data=payload, method="POST",
        headers={"Authorization": f"Bearer {s.github_token}",
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json",
                 "User-Agent": "forja-pipeline"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read()).get("html_url", "")


def _deploy_real(slug: str) -> dict:
    """git branch/commit/push (+PR se houver token). Roda em thread."""
    s = settings()
    root = s.repo_root
    branch = f"{slug}/objeto-educacional"
    _git(["checkout", "-B", branch, s.github_base_branch], root)
    _git(["add", slug, "index.html", "README.md"], root)
    # só commita se há algo staged (evita falha em re-run idempotente)
    tem_staged = subprocess.run(["git", "diff", "--cached", "--quiet"],
                                cwd=str(root)).returncode != 0
    if tem_staged:
        _git(["commit", "-m", _commit_msg(slug)], root)
    pushed = False
    pr_url = ""
    if s.has_github_token:
        _git(["push", "-u", "origin", branch], root)
        pushed = True
        pr_url = _abrir_pr_rest(slug, branch)
    return {"branch": branch, "pushed": pushed, "pr_url": pr_url}


async def deploy(state: PipelineState, config) -> dict:
    s = settings()
    slug = state["slug"]
    branch = f"{slug}/objeto-educacional"
    await emit(config, "deploy", "running", "Aprovado — publicando…")

    if s.dry_run:
        plano = (f"[DRY-RUN] git checkout -B {branch} {s.github_base_branch}\n"
                 f"          git add {slug} index.html README.md\n"
                 f'          git commit -m "{_commit_msg(slug)}"\n'
                 f"          git push -u origin {branch}\n"
                 f"          PR: {branch} → {s.github_base_branch} "
                 f"({'via REST' if s.has_github_token else 'sem token — push-only'})")
        await emit(config, "deploy", "ok", "Dry-run: nada publicado (plano abaixo).",
                   {"branch": branch, "pr_url": "(dry-run)", "plano": plano})
        return {"branch": branch, "pr_url": "(dry-run)", "status_final": "sucesso"}

    try:
        res = await asyncio.to_thread(_deploy_real, slug)
    except Exception as e:  # noqa: BLE001
        await emit(config, "deploy", "fail", f"Falha no deploy: {e}")
        raise

    if res["pr_url"]:
        await emit(config, "deploy", "ok", f"PR aberto: {res['pr_url']}", res)
    elif res["pushed"]:
        await emit(config, "deploy", "ok", f"Branch {branch} enviada (abra o PR).", res)
    else:
        await emit(config, "deploy", "ok",
                   f"Commit em {branch} (sem token: sem push/PR).", res)
    return {"branch": branch, "pr_url": res["pr_url"], "status_final": "sucesso"}


async def notificar_falha(state: PipelineState, config) -> dict:
    erros = state.get("erros_validacao", [])
    await emit(config, "deploy", "skip",
               f"Falha após {state.get('tentativas_correcao', 0)} tentativas. Deploy cancelado.",
               {"erros": erros})
    return {"status_final": "falha"}
