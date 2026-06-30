# A Forja — Console do Pipeline (LangGraph + DeepSeek/Gemini)

Aplicação web que dispara, monitora, valida e **aprova (human-in-the-loop)** a
geração automática dos objetos educacionais mapa-metáfora deste repositório.
Por baixo, um grafo LangGraph executa o pipeline e abre um Pull Request ao final.

```
definir_slug → gerar_prompt(DeepSeek) → gerar_imagem(Gemini) → gerar_objeto(DeepSeek)
   → validar_objeto(Playwright) → [loop autocorreção, máx. 3] → atualizar_atlas
   → [interrupt_before=deploy: aprovação humana] → deploy (abre PR)
```

## Estado atual — Fase 1 (scaffolding)

Esqueleto **funcional ponta a ponta** com nós em modo *stub* (sem chamar as APIs
ainda). Já valem de verdade: o grafo LangGraph, o roteamento condicional, o
**loop de autocorreção**, o **gate HITL** (`interrupt_before=["deploy"]`), a
persistência (`AsyncSqliteSaver`), os eventos **SSE** e a **injeção do JSON no
template fixo** (correção A1). As correções A2 (marcadores-sentinela) e A3
(seletor `[data-conceito]` em `#figura`) já estão preparadas no repositório.

Fases seguintes ligam as APIs reais (DeepSeek/Gemini), o Playwright e o deploy via
GitHub MCP — ver o plano em `/root/.claude/plans`.

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
