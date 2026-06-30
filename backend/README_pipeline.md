# A Forja — Console do Pipeline (LangGraph + DeepSeek/Gemini)

Aplicação web que dispara, monitora, valida e **aprova (human-in-the-loop)** a
geração automática dos objetos educacionais mapa-metáfora deste repositório.
Por baixo, um grafo LangGraph executa o pipeline e abre um Pull Request ao final.

```
definir_slug → gerar_prompt(DeepSeek) → gerar_imagem(Gemini) → gerar_objeto(DeepSeek)
   → validar_objeto(Playwright) → [loop autocorreção, máx. 3] → atualizar_atlas
   → [interrupt_before=deploy: aprovação humana] → deploy (abre PR)
```

## Estado atual — pipeline completo

Todos os nós estão **reais**, com fallback seguro quando faltam chaves:

- **gerar_prompt** — DeepSeek (`deepseek-chat`, OpenAI-compatible). Sem chave → stub.
- **gerar_imagem** — Gemini `gemini-2.5-flash-image` (`generate_content` →
  `inline_data.data` → Pillow). Sem chave → PNG placeholder. Retry + guardrail de cota.
- **gerar_objeto (A1)** — DeepSeek em modo JSON emite **só o JSON**; valida o schema
  e injeta no **template fixo** (`render.py`). Sem chave → stub.
- **validar_objeto (A3)** — Playwright real conta `#figura [data-conceito]`, checa
  acessibilidade/modal/tour/`:focus-visible`/`prefers-reduced-motion` e **zero
  requisições externas**; erros realimentam o loop (máx. 3). Sem navegador → check estático.
- **atualizar_atlas (A2)** — insere por **marcadores-sentinela** no `index.html` e
  `README.md` raiz; idempotente.
- **deploy** — git branch/commit/push + PR via **API REST** (`GITHUB_TOKEN`).
  **`FORJA_DRY_RUN=true` (default)** apenas planeja, sem mexer no git nem abrir PR.

Continua valendo a base: grafo LangGraph, roteamento condicional, **loop de
autocorreção**, **gate HITL** (`interrupt_before=["deploy"]`), `AsyncSqliteSaver`, SSE.

> Segurança: em dry-run nada é publicado. Para publicar de verdade (na sua máquina),
> defina `FORJA_DRY_RUN=false` e um `GITHUB_TOKEN` no `.env`.

## Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # preencha DEEPSEEK_API_KEY e GEMINI_API_KEY (Fase 2+)
uvicorn app.main:app --reload --port 8000
```

Endpoints: `POST /runs`, `GET /runs`, `GET /runs/{id}`,
`GET /runs/{id}/stream` (SSE), `POST /runs/{id}/approve|reject|regenerate`,
`GET /objects|/pulls|/providers|/config`, `GET /health`.

## Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev                   # http://localhost:5173 (proxy /api → :8000)
```

9 telas: Visão geral, Execuções, Nova geração, **Console** (trilha do grafo via
SSE + checklist §4.4 + stream + painel HITL), Objetos, Pull Requests,
Modelos & Chaves, Prompts & Template, Configurações.

## Estrutura

```
backend/app/
  main.py  config.py  events.py  runner.py
  api/        runs.py  stream.py  catalog.py
  pipeline/   state.py  graph.py  clients.py  prompts.py  render.py
              templates/objeto.template.html   # template fixo (A1)
              nodes/  slug prompt imagem objeto validar atlas deploy
frontend/src/  App.jsx  components.jsx  theme.css  lib/api.js  views/*.jsx
```
