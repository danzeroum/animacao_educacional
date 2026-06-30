# Pipeline de Geração de Objetos Educacionais

Documento que **registra o processo** de criação dos objetos educacionais (formato mapa-metáfora) e propõe **um pipeline novo, único e à prova de erro**.

---

## 1. Processo atual (registrado)

```
[Você] tema + conhecimento
   │
   ▼
1) Maritaca.ai ......... gera o PROMPT da imagem (metáfora "homens da caverna")
   │  prompt
   ▼
2) Gemini (imagens) .... gera a IMAGEM de fundo do objeto
   │  imagem .png
   ▼
3) Claude Code (GitHub)  recebe: prompt fixo + prompt do Maritaca + imagem
   │
   ▼
4) Claude Code ......... entrega o OBJETO no modelo de `arquitetura-de-software-caverna`
   │                     (+ atualiza index.html e README da raiz)
   ▼
5) [Você] ............. renomeia a imagem do Gemini e sobe na pasta do objeto
   │
   ▼
6) [Você] ............. push no repositório → vê o objeto integrado ao todo
```

**Ferramentas por etapa:** Maritaca.ai (prompt) → Gemini (imagem) → Claude Code + GitHub (código) → GitHub (publicação).

---

## 2. Diagnóstico — onde o processo trava

1. **Nome da imagem é decidido no fim, não no início.** O Claude "sugere" um nome (passo 4) e você renomeia depois (passo 5). Se o nome sugerido e o `<img src>` divergirem por um caractere, a imagem quebra. O objeto é entregue **antes** da imagem existir, então o `<img>` aponta para um arquivo que ainda não está lá.

2. **Hotspots posicionados às cegas.** O Claude posiciona os 12 nichos confiando que a imagem seguiu o layout 5+7. Sem ver a imagem (ou sem um contrato de composição rígido), o alinhamento pode sair torto.

3. **Integração depende de memória.** Atualizar o `index.html` (Atlas) e o `README` (catálogo) da raiz depende do prompt colado lembrar de pedir. Se esquecer, o objeto nasce "órfão" — existe mas não aparece na página principal.

4. **Sem verificação padronizada.** Nada garante que os 12 modais abrem, que o teclado funciona e que não há requisição externa antes de publicar.

5. **Metadados do card sem regra fixa.** `cor`, `nivel`, `tags`, `cat` do card no Atlas são escolhidos a cada vez sem rubrica — gera inconsistência entre objetos.

---

## 3. Pipeline NOVO (recomendado) — passo a passo

> A mudança-chave: **o slug da pasta é definido no início e determina tudo** (nome da imagem, `src`, ids). Nada é "decidido no fim".

### Etapa 0 — Definir o slug (você, 30s)
Decida `tema` + `metáfora` e monte o **slug** em kebab-case sem acento: `{tema}-{metafora}`.
Exemplo: `tech-squads-caverna`.
👉 Esse slug já define: a pasta `{slug}/`, a imagem `{slug}.png`, o `<img src>` e o `id` no Atlas.

### Etapa 1 — Gerar o prompt da imagem (Maritaca.ai)
Peça o prompt **no formato-contrato** (é ele que faz os hotspots encaixarem):
- Proporção **16:9**, preenchendo borda a borda.
- **DUAS FAIXAS** horizontais: **5 nichos em cima**, **7 nichos embaixo**.
- Nichos separados por **PILARES / COLUNAS DE ROCHA**, cada conceito no seu compartimento.
- **SEM TEXTO** (apenas símbolos rupestres abstratos).

### Etapa 2 — Gerar a imagem (Gemini)
Gere a imagem e **já salve como `{slug}.png`** (ex.: `tech-squads-caverna.png`). O nome é determinístico — definido na Etapa 0, não no fim.

### Etapa 3 — Gerar o objeto (Claude Code) — UMA execução, com a imagem anexada
Cole **o prompt fixo aprimorado** (seção 5) + o prompt do Maritaca entre aspas + **anexe a imagem**. O Claude, numa só execução:
- cria `{slug}/index.html` no modelo padrão, com `<img src="{slug}.png">`;
- posiciona os 12 hotspots **conferindo a imagem anexada** (alinha aos pilares reais);
- cria `{slug}/README.md` com a tabela de mapeamento;
- **atualiza o `index.html` da raiz** (novo card no array `DATA` do Atlas);
- **atualiza o `README.md` da raiz** (linha do catálogo);
- roda a **verificação** (seção 4.4).

### Etapa 4 — Subir os arquivos (você)
Faça upload de: `{slug}/index.html`, `{slug}/README.md`, a imagem `{slug}.png` dentro de `{slug}/`, e os `index.html` + `README.md` da raiz atualizados.
👉 Como o nome da imagem já é `{slug}.png`, **não há renomear no fim nem risco de `<img>` quebrada**.

### Etapa 5 — Push e conferência
Atualize o repositório. O objeto **já aparece linkado no Atlas** (`index.html` raiz) e no catálogo, porque a integração foi feita na Etapa 3.

```
Etapa 0 slug ─► 1 prompt (Maritaca) ─► 2 imagem {slug}.png (Gemini)
        └─► 3 Claude Code: objeto + README + ATLAS + catálogo + verificação (1 execução)
        └─► 4 upload (imagem já tem o nome certo) ─► 5 push ─► integrado ✓
```

---

## 4. Regras que tornam o pipeline à prova de erro

### 4.1 Nome de imagem determinístico
A imagem de fundo **sempre** se chama `{slug}.png` (igual ao nome da pasta) e fica **dentro** da pasta do objeto. O `index.html` referencia `<img src="{slug}.png">`. Fim do passo "Claude sugere um nome".

### 4.2 Integração obrigatória (movida para o `CLAUDE.md`)
Como o Claude Code **lê o `CLAUDE.md` automaticamente**, a regra "ao criar um objeto, atualizar o Atlas (`index.html` raiz) e o catálogo (`README` raiz)" deve morar lá — assim acontece **mesmo que o prompt colado esqueça de pedir**. (Edição já aplicada no `CLAUDE.md` que acompanha este documento.)

### 4.3 Contrato de composição da imagem
Sempre 16:9, **5 nichos em cima + 7 embaixo**, separados por pilares. Isso permite uma **geometria de hotspots padrão (GEO)** que encaixa com ajuste mínimo.

### 4.4 Verificação antes de publicar (checklist)
- [ ] Abre no navegador sem erro no console
- [ ] Os 12 modais abrem corretamente
- [ ] O tour guiado percorre todos os nichos
- [ ] Teclado funciona (Tab, Enter, Esc, setas ←→↑↓)
- [ ] **Nenhuma requisição externa** (aba Network vazia / sem CDN)
- [ ] Foco visível (`:focus-visible`) e `prefers-reduced-motion` respeitado
- [ ] `index.html` raiz e `README` raiz atualizados

### 4.5 Metadados padronizados do card do Atlas
Ao adicionar a entrada no array `DATA`:
- **`cat`** (trilha) — escolha **uma** de: `arq` (Arquitetura & Infra), `qual` (Qualidade & Código), `dados` (Dados & IA), `prod` (Produto & Pessoas), `seg` (Segurança & Governança).
- **`cor`** — o acento dominante da imagem/tema (hex).
- **`nivel`** — `Iniciante` / `Intermediário` / `Avançado` (pela profundidade do tema).
- **`tags`** — 3 a 4 conceitos-chave.
- **`cenario`** — a metáfora (`Caverna`, `Aldeia`, `Acampamento`, `Sala de Controle`, `Tribo`…).

---

## 5. Prompt fixo APRIMORADO (copie e cole no Claude Code)

> Cole isto, depois o prompt do Maritaca entre aspas, e **anexe a imagem**.

```
Crie um novo objeto educacional interativo no formato mapa-metáfora, seguindo
EXATAMENTE o modelo de
https://github.com/danzeroum/animacao_educacional/tree/main/arquitetura-de-software-caverna
e as convenções do CLAUDE.md do repositório.

Vou enviar abaixo: (1) entre aspas, o prompt que gerou a imagem (define a metáfora
e os 12 nichos); (2) a imagem PNG anexada (o fundo do objeto).

Regras obrigatórias:
- Slug da pasta = {tema}-{metafora} (kebab, sem acento). Crie {slug}/index.html e
  {slug}/README.md.
- O nome da imagem é DETERMINÍSTICO: use <img src="{slug}.png">. Não sugira outro
  nome — vou subir a imagem exatamente como {slug}.png dentro de {slug}/.
- Use a IMAGEM ANEXADA para posicionar os 12 hotspots sobre os nichos reais
  (5 na faixa superior, 7 na inferior), conferindo o alinhamento com os pilares de rocha.
- Cada conceito: frase que liga a metáfora ao conceito + 3 bullets para devs juniores
  + ferramentas reais (links) + 1 dica acionável + conexões com conceitos relacionados.
- Acessibilidade obrigatória: tabindex/role/aria-label nas estações, :focus-visible,
  aria-live no título do modal, prefers-reduced-motion, navegação por setas, Esc fecha.
  Inclua tour guiado com <progress> e uma legenda numerada como rota alternativa.
- Single-file: CSS e JS inline, SEM CDN, sem dependências externas.
- INTEGRAÇÃO (sempre, na mesma execução):
   • Atualize o index.html da RAIZ adicionando uma entrada no array DATA do Atlas com:
     id={slug}, nome, tema, cenario, icone, cor (acento dominante), n (nº de conceitos),
     cat (uma das trilhas fixas), nivel, tags (3-4), desc (1 linha).
   • Atualize o README.md da RAIZ adicionando a linha do catálogo.
- Verifique antes de entregar: abre sem erro no console; os 12 modais abrem; o tour
  percorre todos; teclado funciona; nenhuma requisição externa.
- No fim, confirme o nome esperado da imagem ({slug}.png) e liste o que foi alterado
  (objeto, index.html raiz, README raiz).
```

---

## 6. Convenção de nome da imagem (resumo)

| Item | Regra | Exemplo |
|---|---|---|
| Pasta | `{tema}-{metafora}/` | `tech-squads-caverna/` |
| Imagem | `{slug}.png` (na pasta do objeto) | `tech-squads-caverna.png` |
| Referência | `<img src="{slug}.png">` | `<img src="tech-squads-caverna.png">` |
| id no Atlas | `{slug}` | `tech-squads-caverna` |

> **Ganho do pipeline novo:** o nome da imagem deixa de ser "sugerido no fim" e passa a ser **conhecido desde a Etapa 0**, eliminando o principal ponto de falha (imagem quebrada) e o passo manual de renomear às cegas.
