# Handoff: Forja — Console do Pipeline (LangGraph + DeepSeek/Gemini)

## Visão geral

Este pacote entrega **(A)** a revisão técnica do plano do pipeline LangGraph e **(B)** o sistema web **Forja** — a aplicação que dispara, monitora, valida e **aprova** (human-in-the-loop) a geração automática de objetos educacionais no formato *mapa-metáfora* do repositório `animacao_educacional`, abrindo um Pull Request ao final.

O objetivo do dev: implementar o **backend** (FastAPI orquestrando o grafo LangGraph) e o **frontend** (a aplicação Forja, recriando os mocks deste pacote no ambiente do projeto).

---

## Sobre os arquivos de design

Os arquivos `.dc.html` deste bundle são **referências de design feitas em HTML** — protótipos que mostram aparência e comportamento pretendidos, **não código de produção para copiar**. A tarefa é **recriar esses designs no ambiente do projeto** (React/Vue/etc. com as bibliotecas e padrões já estabelecidos) ou, se ainda não existir frontend, escolher o framework mais adequado (recomendação: **React + Vite**, consumindo a API por SSE).

- `Forja — App.dc.html` — **a aplicação completa** (9 telas, navegação por sidebar). É a referência principal.
- `Forja — Console do Pipeline.dc.html` — o console de um run isolado, em 3 estados (aprovação / execução / falha). Use como detalhamento da tela "Console".
- `Pipeline Visual.dc.html` / `Pipeline Visual.png` — infográfico do fluxo (documentação/onboarding).
- `referencia/PIPELINE.md` e `referencia/CLAUDE.md` — as regras de negócio que os nós do grafo devem cumprir (contrato de imagem, nome determinístico, integração com o Atlas, checklist de validação).

## Fidelidade

**Alta fidelidade (hi-fi).** Cores, tipografia, espaçamento e estados finais. Recriar a UI fielmente com a biblioteca do codebase. Se não houver design system, os tokens da seção final bastam.

---

# PARTE A — Revisão do plano LangGraph

O esqueleto do plano (State tipado, nós, aresta condicional, retry ≤3, HITL via `interrupt_before`) está **arquiteturalmente correto**. Três pontos são **bloqueantes** e devem entrar antes de codar os nós:

### A1. (BLOQUEANTE) Não gerar o HTML inteiro pela LLM — gerar só o JSON
Um objeto é um single-file de ~40–48 KB (~12–16k tokens de saída). O `max_tokens` da DeepSeek **trunca** isso → arquivo quebrado. 
**Correção:** o nó `gerar_objeto` emite **apenas o JSON** dos 12 conceitos + `GEO` (geometria dos hotspots) + `RELACOES` + metadados. O **Python injeta** esse JSON num **template fixo** (o `index.html` de `arquitetura-de-software-caverna`, com placeholders). Benefícios: elimina truncamento, garante acessibilidade/tour/estrutura idênticos ao padrão, e mantém os hotspots consistentes (o template já tem o layout 5+7).

### A2. (BLOQUEANTE) `atualizar_atlas` não deve usar BeautifulSoup nem nº de linha
O array `DATA` do Atlas é **JavaScript**, não DOM — BS4 não serve, e "~linha 257" quebra ao primeiro reflow. 
**Correção:** inserir por **marcadores-sentinela** já presentes nos arquivos da raiz:
- `index.html` raiz: inserir a nova entrada imediatamente antes de `/* __ATLAS_ENTRIES__ */`.
- `README.md` raiz: inserir a linha do catálogo antes de `<!-- __CATALOGO__ -->`.
(Hoje esses marcadores ainda não existem nos arquivos da raiz — **adicioná-los uma vez** é pré-requisito.)

### A3. (BLOQUEANTE) Seletor do validador inconsistente
`qa-caverna` usa `.hotspot` + `data-conceito`; o plano cita `.estacao`. Como o Playwright executa o JS, **conte os botões renderizados** dentro de `#figura` (ou `[data-conceito]`), não uma classe fixa. Padronize o seletor no template base.

### Confirmações (corretos no plano)
- `from langgraph.checkpoint.memory import MemorySaver` ✓ (e `SqliteSaver` para persistir).
- `interrupt_before=["deploy"]` ✓ — caminho estável para o HITL.
- Gemini imagem via `generate_content` + extrair `inline_data.data` ✓.
- DeepSeek OpenAI-compatible (`base_url=https://api.deepseek.com`, SDK `openai`) ✓.

### Ajustes adicionais
- **Use `SqliteSaver`, não `MemorySaver`**, no servidor web: o `interrupt`/resume cruza requisições HTTP (e pode cruzar restart). Persistir por `thread_id` é obrigatório para o botão "Aprovar" retomar o run certo.
- **Verifique no build** o id exato do modelo de imagem e a cota do free tier (nomes/limites mudam) — não tratar números como fixos. Ter um **guardrail de cota**: capturar erro de quota e interromper o run com status claro.
- **Idempotência:** rodar o mesmo slug sobrescreve a pasta — proteger ou versionar.
- Tratar retry/erro também no `gerar_imagem` (não só no objeto).

### Arquitetura do grafo (referência)
```
definir_slug → gerar_prompt → gerar_imagem → gerar_objeto → validar_objeto
                                                  ▲               │ (conditional)
                                                  └──── erros ────┤ validacao_ok=False & tent<3
                                                                  ├─► atualizar_atlas → [interrupt] → deploy → END
                                                                  └─► notificar_falha → END  (tent>=3)
```

---

# PARTE B — O sistema web Forja

Aplicação de **controle, monitoramento e aprovação** do pipeline. Server orquestra; front consome eventos.

## B0. Arquitetura backend ↔ frontend (contrato)

- **FastAPI + Uvicorn.** O grafo LangGraph roda no servidor; cada nó emite eventos de progresso.
- **Endpoints sugeridos:**
  - `POST /runs` — body `{tema, metafora, max_tentativas, hitl}` → cria run, retorna `{thread_id}`.
  - `GET  /runs` — lista runs (para as telas Execuções/Dashboard).
  - `GET  /runs/{thread_id}` — detalhe (estado dos nós, validação, diffs).
  - `GET  /runs/{thread_id}/stream` — **SSE**: emite `{node, status, payload, ts}` a cada transição (alimenta a trilha do grafo e o log sem polling).
  - `POST /runs/{thread_id}/approve` — retoma `graph.invoke(None, config)` → executa `deploy` (abre PR).
  - `POST /runs/{thread_id}/reject` e `/regenerate` — descarta ou força nova tentativa.
  - `GET  /pulls`, `GET /objects`, `GET /config`, `GET /providers` — telas de catálogo/admin.
- **Checkpointer:** `SqliteSaver` (`./forja.db`), chave `thread_id`.
- **Estados de um nó (enum):** `pending`, `running`, `ok`, `fail`, `skip`, `wait` (este último só para `deploy` no gate HITL).
- **Status de um run (enum):** `Em execução`, `Aguardando aprovação`, `Concluído`, `Falha`.

## B1. Shell da aplicação (todas as telas)

**Layout:** grid de 2 colunas — **sidebar fixa 228px** + área principal. Largura de referência 1400px; a área principal tem **top bar** (título + ação "Nova geração") e **conteúdo rolável**.

**Sidebar:** logo "🔥 A Forja" + 3 grupos de navegação. Item ativo: fundo `rgba(240,210,154,.14)`, texto `#f0d29a`, borda `#6d5b47`. Item inativo: fundo transparente, texto `#cdbb9a`.
> ⚠️ Bug conhecido a evitar na recriação: o realce ativo deve usar `background-color` (longhand), não o shorthand `background`, para o highlight seguir a tela selecionada.

Grupos e telas:
- **Execução:** Visão geral · Execuções · Nova geração · Console
- **Catálogo:** Objetos · Pull Requests
- **Administração:** Modelos & Chaves · Prompts & Template · Configurações

**Estado:** `view` (string) controla a tela ativa; troca via clique na sidebar. `estadoConsole` controla o estado mostrado no Console.

## B2. Telas (propósito + conteúdo)

**1. Visão geral (Dashboard)** — saúde do pipeline.
- 4 KPIs (cards): Execuções `47` (+6 semana); Taxa de sucesso `87%`; Tentativas/run `1.6`; PRs abertos `3`.
- "Saúde do grafo · últimos 30 runs": 7 mini-barras (uma por nó) com % de sucesso (slug 100, prompt 100, imagem 94, objeto 81, validar 87, atlas 100, deploy 100). Barra verde `#7cb87c` / âmbar `#e0b066`.
- "Cota das APIs": barras — DeepSeek grant `2.9M/5M` (58%, `#5fb3d9`); Gemini imagens hoje `112/500` (22%, `#7cb87c`).
- "Execuções recentes": lista clicável (vai ao Console).

**2. Execuções** — tabela de todos os runs. Filtros (chips): Todos/Aguardando/Em execução/Concluído/Falha. Colunas: Slug (mono) · Tema·Metáfora · Status (dot+label colorido) · Tentativas (`2/3`) · Duração · botão "Abrir".

**3. Nova geração** — formulário (2 colunas). Esq.: Tema, Metáfora, **slug ao vivo** (`git-flow-metro` · imagem `git-flow-metro.png`), seletor modelo texto (`deepseek-chat`), modelo imagem (`gemini-2.5-flash-image`), toggle HITL (on), máx. tentativas (`3`), botão "▶ Iniciar geração". Dir.: prévia dos 6 passos do que vai acontecer.

**4. Console do run** — tela central de operação. 
- Header: `run #a1f7 · thread {slug}` + pill de status.
- **Trilha do grafo:** 7 nós em linha (`definir_slug … deploy`), cada um card com ícone, dot de status (pulsa em `running`/`wait`), nome (mono) e label. Setas `▶` entre os nós. Badge "tentativa 2/3" no nó `gerar_objeto`.
- **Validação §4.4** (card): checklist 2 colunas com 8 itens ✓, e nota do loop ("tentativa 1: 3 estações sem aria-label → reinjetado → tentativa 2 corrigiu").
- **Stream de eventos** (card mono, fundo `#0c0703`): linhas `tempo + mensagem` coloridas por status.
- **Painel HITL** (borda azul `#5fb3d9`): lista de arquivos do commit (`+` novos, `~` modificados na raiz), diff da entrada `DATA`, branch→PR, e botões **Aprovar e abrir Pull Request** (primário azul), **Regenerar**, **Descartar**.
- Estados: `Aguardando aprovação` (mostra HITL), `Em execução` (spinner + "Gerando…"), `Falha (3 tentativas)` (lista de erros acumulados, sem deploy).

**5. Objetos (Catálogo)** — grid 3 col de cartões dos objetos gerados. Cada cartão: slug (mono), status de integração (No Atlas `#7cb87c` / PR aberto `#e0b066` / Aguardando `#5fb3d9` / Falha `#cf6a4a`), nome (Cinzel), tema, nº de conceitos, "Abrir →". Topo da tela: "16 de 18 linkados".

**6. Pull Requests** — tabela: `#id` (azul) · slug · branch (`{slug}/objeto-educacional`) · status (Aberto/checks ✓/Merged `#9b7ed6`) · botão "GitHub ↗".

**7. Modelos & Chaves (admin)** — 3 cards: DeepSeek (`DEEPSEEK_API_KEY` mascarada, `deepseek-chat`, base_url, barra grant), Gemini (`GEMINI_API_KEY`, `gemini-2.5-flash-image`, barra cota diária), GitHub (MCP `create_pull_request`, repo). Nota: chaves vêm do `.env`, nunca commitadas.

**8. Prompts & Template (admin)** — prompt-fixo do objeto (bloco mono, com a regra "EMITA APENAS o JSON"); contrato de composição da imagem (16:9, 5+7 nichos, pilares, sem texto); marcadores-sentinela (`/* __ATLAS_ENTRIES__ */`, `<!-- __CATALOGO__ -->`, template base).

**9. Configurações (admin)** — linhas label/valor: Servidor (`localhost:8000`), Eventos (`SSE · /stream`), Checkpointer (`SqliteSaver · ./forja.db`), Aprovação humana (`ATIVO`), Máx. tentativas (`3`), Padrão de branch (`{slug}/objeto-educacional`). Botão "Salvar".

## B3. Interações & comportamento
- Navegação: clique na sidebar troca `view` (sem reload). Top bar "Nova geração" → tela Nova geração; itens/linhas de run → Console.
- Trilha do grafo: dot pulsa (`@keyframes pulse`, 1.4s) em `running`/`wait`. Spinner no estado em execução (`@keyframes spin`, 1s linear).
- Transições devem respeitar `prefers-reduced-motion: reduce` (desligar animações).
- Aprovação: `Aprovar` chama `/approve` → trilha avança `deploy` → status `Concluído` + PR na tela Pull Requests. `Regenerar` → volta `gerar_objeto`. `Descartar` → encerra run.
- Foco visível obrigatório (`:focus-visible`, contorno `#f0d29a`) em todos os elementos focáveis.

## B4. State (frontend)
- `view: string` — tela ativa.
- `runs: Run[]`, `run: RunDetail` (nós, validação, log, diffs), `objects`, `pulls`, `providers`, `config` — vindos da API.
- `consoleState` derivado de `run.status`.
- Stream SSE atualiza `run.nodes[*].status` e `run.log` em tempo real.

---

## Design tokens

**Cores**
- Fundo (gradiente radial): `#241710` → `#16100a` → `#0e0905`. Painéis: `rgba(20,13,7,.5)`. Cartões: `linear-gradient(180deg, rgba(45,30,17,.85), rgba(20,13,7,.85))`.
- Bordas: `#3a2c1e` (sutil), `#6d5b47` (média), `#2a2018` (divisores).
- Texto: `#f0e6d2` (claro), `#cdbb9a` / `#d9c4a0` (corpo), `#a89576` / `#8a7350` (mudo), `#6d5b47` (fraco).
- Dourado/acento: `#f0d29a` (primário), `#e0b066` / `#b9925a`.
- Status: ok `#7cb87c` · running/atenção `#e0b066` · waiting/info `#5fb3d9` · fail `#cf6a4a` · merged/roxo `#9b7ed6` · pending `#6d5b47`.

**Tipografia**
- Display/títulos/labels: **Cinzel** (600/700), uppercase com `letter-spacing` .06–.2em nos kickers.
- Corpo: **Spectral** (400/600).
- Código/mono/logs/slugs: `ui-monospace, Menlo, monospace`.
- Escala: KPI 30px/700; título tela 18px/700; títulos card 12–14px; corpo 12.5–13.5px; mono 11–12px.

**Raio & espaçamento**
- Raio: cards 13–16px, inputs/chips/botões 8–10px, dots 50%.
- Padding: telas 24–26px; cards 15–22px; gap de grids 16–22px.
- Sidebar 228px; top bar ~58px; largura de referência 1400px.

**Sombra/efeitos:** cartões usam apenas borda + leve gradiente (sem sombras pesadas). Glows opcionais via `radial-gradient` de baixa opacidade. `color-mix(in srgb, <cor> X%, transparent)` para tints de status.

## Assets
Nenhum binário além de `Pipeline Visual.png` (doc). Ícones são **emojis** (consistente com o repo `animacao_educacional`). Fontes Cinzel/Spectral via Google Fonts — no codebase, usar o mecanismo de fontes do projeto (ou `@font-face` self-hosted).

## Arquivos neste bundle
- `Forja — App.dc.html` — app completo (referência principal).
- `Forja — Console do Pipeline.dc.html` — console detalhado, 3 estados.
- `Pipeline Visual.dc.html` + `Pipeline Visual.png` — infográfico do fluxo.
- `referencia/PIPELINE.md`, `referencia/CLAUDE.md` — regras que os nós do grafo devem cumprir.

> Os `.dc.html` abrem direto no navegador para inspeção visual. Use-os como referência de pixel; a lógica real (grafo + APIs) é descrita na Parte A e B0.
