# Métodos Ágeis na Caverna — Agilidade Pré-Histórica para Devs Juniores

Objeto educacional no formato **mapa-metáfora**: uma única ilustração de caverna pré-histórica em corte transversal onde **a própria figura é a interface**. Cada nicho da arte rupestre é um hotspot interativo que ensina um conceito de métodos ágeis. A cena se divide em uma faixa **Superior** (fluxo visual e planejamento: Kanban, BDD, Burndown, WSJF, DoD) e uma faixa **Inferior** (gestão de entrega: Backlog, Critérios de Aceite, Lead Time, Cycle Time, Throughput, Gargalos, Inception). Em vez de 12 definições isoladas, o aluno aprende por **espaço e ritual** — vendo como cada prática se encaixa no sistema de entrega da tribo. Voltado para devs juniores.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador — sem instalação, sem servidor, sem build. O arquivo `metodos-ageis-caverna.png` (a ilustração) precisa ficar na mesma pasta que o `index.html`. Clique em qualquer nicho da caverna, use a **legenda numerada** (rota acessível alternativa) ou o **Tour guiado** para uma visita automática pelos 12 conceitos.

### Realces e Conexões

Ao abrir um conceito, os nichos relacionados pulsam com contorno tracejado e o modal traz a seção **🔗 Conecta-se com**, com chips clicáveis que saltam entre os conceitos — materializando como Kanban, métricas de fluxo e práticas de qualidade formam um sistema integrado.

### Acessibilidade

Hotspots são `<button>` com `aria-label`, navegáveis por Tab/Enter e com foco visível; a legenda numerada é a rota alternativa para quem não percebe as regiões sobre a arte; `Esc` fecha o modal; com o Tour ativo, `←`/`→` navegam manualmente; e `prefers-reduced-motion` desliga as animações de pulso/halo.

## Mapeamento

### Faixa Superior — Fluxo Visual e Planejamento

| Região da ilustração | Conceito técnico |
|---|---|
| 🟦 Quadro com colunas de pedras coloridas | Kanban (visualização do fluxo, WIP Limit) |
| 🔮 Sequência de símbolos causa-efeito | BDD / Given-When-Then (comportamento esperado) |
| 📉 Linha de sílex descendente | Burndown Chart (progresso da sprint) |
| ⚖️ Balança de valor e tempo | WSJF / Custo do Atraso (priorização por valor) |
| ✅ Lista de entalhes verificados | Definition of Done (critério de qualidade) |

### Faixa Inferior — Gestão de Entrega e Métricas

| Região da ilustração | Conceito técnico |
|---|---|
| 📋 Pilha de tábuas ordenadas | Product Backlog Priorizado |
| 🎯 Marcas de aprovação em pedra | Critérios de Aceite |
| ⏳ Rastro de comprimento total (avistamento → mesa) | Lead Time |
| 🔄 Trecho ativo da trilha de caça | Cycle Time |
| 🏹 Entalhes de entregas completadas | Throughput |
| 🪨 Pedra obstruindo a passagem | Gargalos e Restrições de Fluxo |
| 🔥 Roda de fogueira com a tribo reunida | Inception / Alinhamento de Equipe |
