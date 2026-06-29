# Convenção de Objetos Educacionais

Este repositório armazena objetos educacionais interativos no formato **mapa-metáfora** para devs juniores. Cada objeto vive em sua própria pasta na raiz do repositório.

Ao receber um prompt para criar um novo objeto educacional, siga esta convenção sem precisar perguntar ao usuário onde criar ou como nomear.

---

## 1. Nomenclatura de Pastas

**Formato:** `{tema}-{metafora}/` — kebab-case, português sem acentos.

Derive o nome a partir do prompt:
1. Identifique o **tema** (assunto técnico) e a **metáfora** especificada
2. Slugifique: minúsculas, remova acentos, substitua espaços por hífens
3. Crie a pasta na raiz do repositório

**Exemplos:**

| Prompt | Pasta |
|---|---|
| "observabilidade, metáfora sala de controle" | `observabilidade-sala-de-controle/` |
| "git flow, metáfora metrô" | `git-flow-metro/` |
| "kubernetes, metáfora cidade" | `kubernetes-cidade/` |
| "docker containers, metáfora navio de carga" | `docker-navio-de-carga/` |
| "CI/CD, metáfora linha de montagem" | `cicd-linha-de-montagem/` |

---

## 2. Estrutura Interna de Cada Pasta

```
{tema}-{metafora}/
├── index.html   ← objeto educacional completo (single-file)
└── README.md    ← descrição, mapeamento e instrução de uso
```

### `index.html` — padrão obrigatório

- **Single-file HTML autocontido**: CSS e JS inline, sem dependências externas, sem CDN
- Abre diretamente no navegador com duplo clique
- **Formato mapa-metáfora**: SVG inline representando a metáfora, com estações clicáveis
- Cada estação = 1 conceito técnico
- Modal por conceito com:
  - Frase conectando o elemento da metáfora ao conceito
  - 3 bullets explicativos em linguagem acessível para devs juniores
  - Links de ferramentas relevantes (`ferramentas: [{nome, url}]`)
  - "Dica DevOps/SRE" — recomendação prática acionável
- **Tour guiado** automático com `<progress>` visual
- **Acessibilidade obrigatória:**
  - `tabindex="0"`, `role="button"`, `aria-label` em todas as estações
  - `:focus-visible` para outline de teclado (nunca `outline: none` no `:focus`)
  - `aria-live="polite"` no título do modal
  - `@media (prefers-reduced-motion: reduce)` desligando todas as animações
  - Navegação por setas ←→↑↓ entre estações
  - Escape fecha o modal
- **Meta OG tags** no `<head>` para preview ao compartilhar

### `README.md` — por objeto

```markdown
# {Título} — {Subtítulo com a metáfora}

{1 parágrafo descrevendo o objeto, o tema, a metáfora e o público}

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador.

## Mapeamento

| {Elemento da metáfora} | {Conceito técnico} |
|---|---|
| ...                    | ...                |
```

---

## 3. Branch e PR

- **Branch:** `{tema}-{metafora}/objeto-educacional`
  - Exemplos: `git-flow-metro/objeto-educacional`, `kubernetes-cidade/objeto-educacional`
- **Commits:** mensagens em inglês, prefixo `feat:` para criação, `improve:` para melhorias
- **PR:** base `main`, merge por squash, título em português descrevendo o tema e a metáfora
- **Após merge:** atualizar `README.md` raiz (catálogo) com o novo objeto

---

## 4. Catálogo Raiz

Após criar e mergear um novo objeto, adicione uma linha ao `README.md` da raiz do repositório na tabela de catálogo.

---

## 5. Checklist antes de commitar

- [ ] Pasta nomeada corretamente (`{tema}-{metafora}/`)
- [ ] `index.html` abre no navegador sem erros no console
- [ ] Todas as 6+ estações abrem modal corretamente
- [ ] Tour guiado percorre todas as estações
- [ ] Navegação por teclado funciona (Tab, Enter, Escape, setas)
- [ ] Nenhuma requisição externa na aba Network do DevTools
- [ ] `README.md` dentro da pasta com tabela de mapeamento
- [ ] `README.md` raiz atualizado no catálogo
