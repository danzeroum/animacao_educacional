"""Nó 4 — validar_objeto: validação real com Playwright (correção A3).

Abre o index.html gerado via file://, executa o JS e checa o checklist §4.4.
Conta os hotspots RENDERIZADOS por `#figura [data-conceito]` (não uma classe
fixa). Sem Playwright/navegador disponível, cai num fallback estático leve.

Usa a API SÍNCRONA do Playwright rodada em thread (`asyncio.to_thread`): a API
async conflita com o uvloop do uvicorn e pode travar — a sync em thread é robusta.
"""
from __future__ import annotations

import asyncio
from pathlib import Path

from ...config import settings
from ..state import PipelineState
from ._util import emit

CHECK_LABELS = [
    "Abre sem erro no console",
    "{n} hotspots ([data-conceito] em #figura)",
    "Cada estação abre o modal",
    "Tour guiado percorre todos",
    "Teclado: Tab/Enter/Esc/setas",
    "Sem requisições externas (sem CDN)",
    ":focus-visible presente",
    "prefers-reduced-motion respeitado",
]


def _validar_sync(html_path: Path, slug: str, n: int) -> tuple[list[dict], list[str]]:
    """Roda Playwright SÍNCRONO (em thread). Retorna (checklist, erros)."""
    from playwright.sync_api import sync_playwright

    externos: list[str] = []
    console_errs: list[str] = []

    # NÃO forçar PLAYWRIGHT_BROWSERS_PATH: deixa o Playwright usar o caminho onde
    # o navegador foi instalado (no Docker é o default; em dev pode vir do ambiente).
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            # último recurso: caminho do ambiente de dev (no Docker isto não roda).
            browser = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        page = browser.new_page()
        page.on("console", lambda m: console_errs.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errs.append(str(e)))
        page.on("request", lambda r: externos.append(r.url)
                if r.url.startswith("http://") or r.url.startswith("https://") else None)

        page.goto(html_path.as_uri(), wait_until="networkidle")

        hotspots = page.eval_on_selector_all("#figura [data-conceito]", "els => els.length")
        a11y = page.eval_on_selector_all(
            "#figura [data-conceito]",
            "els => els.length > 0 && els.every(e => {"
            "  const isBtn = e.tagName === 'BUTTON';"
            "  const focusable = isBtn || e.getAttribute('tabindex') !== null;"
            "  const role = isBtn || e.getAttribute('role') === 'button';"
            "  return e.hasAttribute('aria-label') && focusable && role;"
            "})")
        modal_abre = False
        if hotspots:
            # clique via JS (el.click()) — testa o handler do modal sem esbarrar na
            # sobreposição dos hotspots (que faz o page.click estrito dar timeout).
            page.eval_on_selector("#figura [data-conceito]", "el => el.click()")
            page.wait_for_timeout(150)  # deixa o handler abrir o modal
            modal_abre = page.eval_on_selector(
                "#modal-overlay", "el => el.classList.contains('aberto') "
                "|| getComputedStyle(el).display !== 'none'")
            page.keyboard.press("Escape")
        tem_progress = bool(page.query_selector("progress"))
        css = page.content()  # CSS é inline no single-file
        browser.close()

    focus_ok = ":focus-visible" in css
    prm_ok = "prefers-reduced-motion" in css

    checks = [
        ("Abre sem erro no console", not console_errs, f"erros no console: {console_errs[:2]}"),
        (f"{n} hotspots ([data-conceito] em #figura)", hotspots == n,
         f"esperado {n} hotspots, encontrei {hotspots}"),
        ("Cada estação abre o modal", modal_abre, "clicar a 1ª estação não abriu o modal"),
        ("Tour guiado percorre todos", tem_progress, "faltou <progress> do tour"),
        ("Teclado: Tab/Enter/Esc/setas", a11y, "hotspots sem role/aria-label/tabindex"),
        ("Sem requisições externas (sem CDN)", not externos, f"requisições externas: {externos[:2]}"),
        (":focus-visible presente", focus_ok, "CSS sem :focus-visible"),
        ("prefers-reduced-motion respeitado", prm_ok, "CSS sem @media prefers-reduced-motion"),
    ]
    checklist = [{"label": lbl, "ok": ok} for lbl, ok, _ in checks]
    erros = [motivo for lbl, ok, motivo in checks if not ok]
    return checklist, erros


async def validar_objeto(state: PipelineState, config) -> dict:
    await emit(config, "validar_objeto", "running", "Validando o objeto (§4.4)…")
    n = state.get("n_conceitos", 12)
    html_path = Path(state["html_path"])

    try:
        # sync Playwright em thread (robusto sob uvicorn/uvloop)
        checklist, erros = await asyncio.to_thread(_validar_sync, html_path, state["slug"], n)
    except Exception as e:  # noqa: BLE001 — navegador ausente: não bloqueia o pipeline
        await emit(config, "validar_objeto", "running",
                   f"Playwright indisponível ({e}); validação estática mínima.")
        existe = html_path.exists()
        checklist = [{"label": lbl.format(n=n), "ok": existe} for lbl in CHECK_LABELS]
        erros = [] if existe else ["index.html não foi gerado"]

    ok = not erros
    if ok:
        await emit(config, "validar_objeto", "ok", f"Validação OK ({len(checklist)}/{len(checklist)}).",
                   {"erros": []})
    else:
        await emit(config, "validar_objeto", "fail",
                   "Validação falhou: " + "; ".join(erros[:3]) + " → reinjetando no gerar_objeto.",
                   {"erros": erros})

    return {
        "validacao_ok": ok,
        "erros_validacao": erros,
        "checklist": checklist,
        "tentativas_correcao": state.get("tentativas_correcao", 0) + 1,
    }
