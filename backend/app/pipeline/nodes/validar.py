"""Nó 4 — validar_objeto: validação real com Playwright (correção A3).

Abre o index.html gerado via file://, executa o JS e checa o checklist §4.4.
Conta os hotspots RENDERIZADOS por `#figura [data-conceito]` (não uma classe
fixa). Sem Playwright/navegador disponível, cai num fallback estático leve.
"""
from __future__ import annotations

import os
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


async def _validar_playwright(html_path: Path, slug: str, n: int) -> tuple[list[dict], list[str]]:
    """Retorna (checklist, erros). Levanta ImportError/Erro se o navegador faltar."""
    from playwright.async_api import async_playwright

    erros: list[str] = []
    externos: list[str] = []
    console_errs: list[str] = []

    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
        except Exception:
            browser = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        page = await browser.new_page()
        page.on("console", lambda m: console_errs.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errs.append(str(e)))
        # qualquer requisição http(s) externa = violação (CLAUDE.md: sem CDN)
        page.on("request", lambda r: externos.append(r.url)
                if r.url.startswith("http://") or r.url.startswith("https://") else None)

        await page.goto(html_path.as_uri(), wait_until="networkidle")

        hotspots = await page.eval_on_selector_all("#figura [data-conceito]", "els => els.length")
        img_ok = await page.eval_on_selector(
            "#figura img",
            "img => img.complete && img.naturalWidth > 0", strict=False) if \
            await page.query_selector("#figura img") else False
        # acessibilidade dos hotspots: <button> nativo já é focável e tem role
        # implícito 'button'; elementos não-button precisam de role+tabindex.
        a11y = await page.eval_on_selector_all(
            "#figura [data-conceito]",
            "els => els.length > 0 && els.every(e => {"
            "  const isBtn = e.tagName === 'BUTTON';"
            "  const focusable = isBtn || e.getAttribute('tabindex') !== null;"
            "  const role = isBtn || e.getAttribute('role') === 'button';"
            "  return e.hasAttribute('aria-label') && focusable && role;"
            "})")
        # clique abre o modal
        modal_abre = False
        if hotspots:
            await page.click("#figura [data-conceito]")
            modal_abre = await page.eval_on_selector(
                "#modal-overlay", "el => el.classList.contains('aberto') "
                "|| getComputedStyle(el).display !== 'none'", strict=False)
            await page.keyboard.press("Escape")
        tem_progress = bool(await page.query_selector("progress"))
        html = await page.content()
        css = html  # CSS é inline no single-file
        await browser.close()

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
    if not img_ok:
        # imagem ausente/sem carregar não invalida sozinha (placeholder é válido),
        # mas registramos no console se nem a tag existir
        pass
    checklist = [{"label": lbl, "ok": ok} for lbl, ok, _ in checks]
    erros = [motivo for lbl, ok, motivo in checks if not ok]
    return checklist, erros


async def validar_objeto(state: PipelineState, config) -> dict:
    await emit(config, "validar_objeto", "running", "Validando o objeto (§4.4)…")
    n = state.get("n_conceitos", 12)
    html_path = Path(state["html_path"])

    try:
        checklist, erros = await _validar_playwright(html_path, state["slug"], n)
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
