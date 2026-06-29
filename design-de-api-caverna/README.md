# A Caverna das APIs — Design de API na Idade da Pedra

Objeto educacional no formato **mapa-metáfora**: uma única ilustração coesa de uma caverna pré-histórica em corte transversal onde **a própria figura é a interface**. Cada nicho de rocha é um hotspot interativo que ensina uma boa prática de design de API. A cena se divide em uma faixa **Macro** (a tribo das APIs: métodos HTTP, nomeação de recursos, anti-patterns, observabilidade e open banking) e uma faixa **Micro** (as práticas da caverna: versionamento, rate limiting, segurança, plugins, hooks, ciclo de vida e respostas claras). Em vez de 12 caixas isoladas, o aluno aprende por **espaço e história** — vendo como cada decisão se conecta às vizinhas. Voltado para devs juniores.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador — sem instalação, sem servidor, sem build. O arquivo `design-de-api-caverna.png` (a ilustração) precisa ficar na mesma pasta que o `index.html`. Clique em qualquer nicho da caverna, use a **legenda numerada** (rota acessível alternativa) ou o **Tour guiado** para uma visita automática pelos 12 conceitos.

### Realces Macro ↔ Micro

Ao abrir um conceito, a figura "acende" o sub-sistema: o nicho ativo ganha halo forte, os relacionados pulsam com contorno tracejado e o resto é atenuado. O modal traz a seção **🔗 Conecta-se com**, com uma nota explicando o laço e chips clicáveis que saltam entre os conceitos relacionados — materializando, por exemplo, como rate limiting, segurança e respostas claras cobrem juntos os buracos da "caverna disfuncional".

### Acessibilidade

Hotspots são `<button>` com `aria-label`, navegáveis por Tab/Enter e com foco visível; a legenda numerada é a rota alternativa para quem não percebe as regiões sobre a arte; `Esc` fecha o modal; com o Tour ativo, `←`/`→` navegam manualmente; e `prefers-reduced-motion` desliga as animações de pulso/halo.

## Mapeamento

### Macro — A Tribo das APIs

| Região da ilustração | Conceito técnico |
|---|---|
| 🏺 Trogloditas com gestos distintos sobre a urna (lupa, depositar, trocar, polir, esvaziar) | Métodos HTTP (GET, POST, PUT, PATCH, DELETE) |
| 🐟 Mural de pictogramas autoexplicativos (peixe, fogo, ferramenta) | Nomeação de recursos (substantivos claros, hierarquia) |
| ⚠️ Caverna disfuncional: portão arrombado, tábuas conflitantes, mural em branco, passagem oculta | Anti-patterns de API (sem rate limit, sem versão, sem log, endpoints ocultos) |
| 🔥 Ancião no painel triplo: tambor de pedrinhas, termômetro, corda de nós | Observabilidade (logs, métricas, tracing) |
| 🌉 Duas tribos trocando cestas por uma ponte padronizada, guardião duplo no centro | Open banking / integração entre sistemas (contratos, OAuth) |

### Micro — As Práticas da Caverna

| Região da ilustração | Conceito técnico |
|---|---|
| 📚 Pilha de tábuas em camadas com símbolo de versão | Versionamento de API (evoluir sem quebrar) |
| 🦴 Portão com roleta de ossos e fila por ciclo | Rate limiting (token bucket, 429 Retry-After) |
| 🔑 Guardião com colar de ossos-chave e fechaduras correspondentes | Segurança — autenticação e autorização (tokens, menor privilégio) |
| 🧩 Estrutura central com encaixes laterais padronizados | Plugin architecture (ponto de entrada e encaixes) |
| 🪝 Gancho de osso que dispara reação em cadeia no nicho vizinho | Hooks e extensibilidade (webhooks, pontos de extensão) |
| ♻️ Troglodita removendo um módulo e inserindo outro, comparando formatos | Gerenciamento de ciclo de vida (instalar, atualizar, aposentar) |
| 👍 Gestos de status: polegar, mão aberta, confusão, rosto com fumaça | Respostas claras (famílias HTTP 2xx/3xx/4xx/5xx) |

## Créditos de design

A ilustração `design-de-api-caverna.png` (caverna pré-histórica em corte transversal, sem texto queimado na arte) acompanha o objeto. Para honrar a regra do projeto de **zero dependências externas**, as fontes do estilo (Cinzel/Spectral) são substituídas por uma stack serif do sistema — nenhuma requisição de rede é feita ao abrir o objeto. As posições dos hotspots (`GEO` no `index.html`) são estimadas pela grade de 3 linhas da arte e podem ser ajustadas em % para casar exatamente com o PNG.
