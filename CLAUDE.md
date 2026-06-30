# Convenção de Objetos Educacionais

Este repositório armazena objetos educacionais interativos no formato **mapa-metáfora** para devs juniores. Cada objeto vive em sua própria pasta na raiz do repositório.

Ao receber um prompt para criar um novo objeto educacional, siga esta convenção sem precisar perguntar ao usuário onde criar ou como nomear.

> A página inicial do repositório é o **Atlas** (`index.html` na raiz): um acervo navegável que lista todos os objetos. **Todo objeto novo precisa ser integrado a ele** — ver seção 4.

---

## 1. Nomenclatura de Pastas

**Formato:** `{tema}-{metafora}/` — kebab-case, português sem acentos. Chamamos esse nome de **slug**.

Derive o slug a partir do prompt:
1. Identifique o **tema** (assunto técnico) e a **metáfora** especificada
2. Slugifique: minúsculas, remova acentos, substitua espaços por hífens
3. Crie a pasta na raiz do repositório

**Exemplos:**

| Prompt | Pasta (slug) |
|---|---|
| "observabilidade, metáfora sala de controle" | `observabilidade-sala-de-controle/` |
| "tech squads, metáfora caverna" | `tech-squads-caverna/` |
| "git flow, metáfora metrô" | `git-flow-metro/` |
| "kubernetes, metáfora cidade" | `kubernetes-cidade/` |

---

## 2. Estrutura Interna de Cada Pasta

```
{slug}/
├── index.html   ← objeto educacional completo (single-file)
├── {slug}.png   ← imagem de fundo (mesmo nome da pasta)
└── README.md    ← descrição, mapeamento e instrução de uso
```

### Nome da imagem é DETERMINÍSTICO

A imagem de fundo **sempre** se chama `{slug}.png` (igual ao nome da pasta) e fica **dentro** da pasta do objeto. O `index.html` referencia `<img src="{slug}.png">`. **Nunca** invente outro nome nem peça para o usuário escolher — o nome é conhecido a partir do slug.
Exemplo: pasta `tech-squads-caverna/` → imagem `tech-squads-caverna.png` → `<img src="tech-squads-caverna.png">`.

### `index.html` — padrão obrigatório

- **Single-file HTML autocontido**: CSS e JS inline, sem dependências externas, sem CDN
- Abre diretamente no navegador com duplo clique
- **Formato mapa-metáfora**: a imagem `{slug}.png` é o fundo, com estações (hotspots) clicáveis posicionadas sobre os nichos
- Composição padrão da imagem: **16:9, 2 faixas — 5 nichos em cima, 7 embaixo**, separados por pilares de rocha. Posicione os hotspots conforme a imagem fornecida (confira o alinhamento com os pilares reais).
- Cada estação = 1 conceito técnico
- Modal por conceito com:
  - Frase conectando o elemento da metáfora ao conceito
  - 3 bullets explicativos em linguagem acessível para devs juniores
  - Links de ferramentas relevantes (`ferramentas: [{nome, url}]`)
  - Dica prática acionável
  - Conexões com conceitos relacionados (chips clicáveis)
- **Tour guiado** automático com `<progress>` visual
- **Legenda numerada** como rota acessível alternativa aos hotspots
- **Acessibilidade obrigatória:**
  - `tabindex="0"`, `role="button"`, `aria-label` em todas as estações
  - `:focus-visible` para outline de teclado (nunca `outline: none` no `:focus`)
  - `aria-live="polite"` no título do modal
  - `@media (prefers-reduced-motion: reduce)` desligando todas as animações
  - Navegação por setas ←→↑↓ entre estações; `Esc` fecha o modal
- **Meta OG tags** no `<head>` para preview ao compartilhar

### `README.md` — por objeto

```markdown
# {Título} — {Subtítulo com a metáfora}

{1 parágrafo descrevendo o objeto, o tema, a metáfora e o público}

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador. A imagem `{slug}.png` deve estar na mesma pasta.

## Mapeamento

| {Elemento da metáfora} | {Conceito técnico} |
|---|---|
| ...                    | ...                |
```

---

## 3. Branch e PR

- **Branch:** `{slug}/objeto-educacional`
- **Commits:** mensagens em inglês, prefixo `feat:` para criação, `improve:` para melhorias
- **PR:** base `main`, merge por squash, título em português descrevendo o tema e a metáfora

---

## 4. Integração com o Atlas e o Catálogo (OBRIGATÓRIO)

Ao criar **qualquer** objeto novo, faça também — **na mesma execução**, antes de finalizar — as duas integrações abaixo. Um objeto que não aparece no Atlas nasce "órfão".

### 4.1 Atlas — `index.html` da raiz

Adicione **uma entrada** ao array `DATA` (dentro do `<script>` do `index.html` raiz), no mesmo formato das demais:

```js
{ id:'{slug}', nome:'{Título do objeto}', tema:'{Tema curto}',
  cenario:'{Caverna|Aldeia|Acampamento|Sala de Controle|Tribo}', icone:'🪨',
  cor:'#hex',           // acento dominante da imagem/tema
  n:12,                 // nº de conceitos
  cat:'{trilha}',       // arq | qual | dados | prod | seg
  nivel:'{Iniciante|Intermediário|Avançado}',
  tags:['...','...','...'],   // 3-4 conceitos-chave
  desc:'Uma linha que desperta interesse.' },
```

Trilhas (`cat`) válidas: `arq` (Arquitetura & Infra), `qual` (Qualidade & Código), `dados` (Dados & IA), `prod` (Produto & Pessoas), `seg` (Segurança & Governança).
O card do Atlas linka automaticamente para `{slug}/index.html`.

### 4.2 Catálogo — `README.md` da raiz

Adicione uma linha à tabela de catálogo do `README.md` da raiz, com link para `./{slug}/`.

---

## 5. Checklist antes de commitar

- [ ] Pasta nomeada corretamente (`{slug}/`)
- [ ] Imagem referenciada como `<img src="{slug}.png">`
- [ ] `index.html` abre no navegador sem erros no console
- [ ] Todas as estações (5 + 7) abrem o modal corretamente
- [ ] Tour guiado percorre todas as estações
- [ ] Navegação por teclado funciona (Tab, Enter, Escape, setas)
- [ ] **Nenhuma requisição externa** na aba Network do DevTools (sem CDN)
- [ ] `README.md` dentro da pasta com tabela de mapeamento
- [ ] **`index.html` da raiz (Atlas) atualizado** com a nova entrada no array `DATA` (seção 4.1)
- [ ] **`README.md` da raiz (catálogo) atualizado** (seção 4.2)
- [ ] No fim, confirme o nome esperado da imagem (`{slug}.png`) e liste os arquivos alterados
