# A Caverna dos Squads — Formação e Gestão de Tech Squads na Idade da Pedra

Objeto educacional no formato **mapa-metáfora**: uma ilustração coesa de uma caverna pré-histórica em corte transversal onde **a própria figura é a interface**. Cada nicho da arte é um hotspot interativo que ensina um conceito de formação e gestão de tech squads. A cena se divide em uma faixa **Macro** (o squad completo: multifuncionalidade, OKR, liderança situacional, autogestão, alinhamento de responsabilidades) e uma faixa **Micro** (dinâmica e competências: as quatro fases de Tuckman, code review, skills matrix e plano de desenvolvimento). Voltado para devs juniores e tech leads em formação.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador — sem instalação, sem servidor, sem build. O arquivo `tech-squads-caverna.png` (a ilustração) precisa ficar na mesma pasta que o `index.html`. Clique em qualquer nicho da caverna, use a **legenda numerada** (rota acessível alternativa) ou o **Tour guiado** para uma visita automática pelos 12 conceitos.

### Realces Macro ↔ Micro

Ao abrir um conceito, a figura "acende" o subsistema: o nicho ativo ganha halo forte, os relacionados pulsam com contorno tracejado e o resto é atenuado. O modal traz a seção **🔗 Conecta-se com**, com uma nota explicando o laço e chips clicáveis que saltam entre os conceitos relacionados.

### Acessibilidade

Hotspots são `<button>` com `tabindex="0"`, `role="button"` e `aria-label`, navegáveis por Tab/Enter e com foco visível; a legenda numerada é a rota alternativa para quem não percebe as regiões sobre a arte; `Esc` fecha o modal; com o Tour ativo, `←`/`→` navegam manualmente; e `prefers-reduced-motion` desliga as animações de pulso/halo.

## Mapeamento

### Macro — O Squad Completo (faixa superior)

| Nicho da ilustração | Conceito técnico |
|---|---|
| 🔥 Círculo de trogloditas com ferramentas distintas | Squad Multifuncional (competências complementares, T-shape) |
| 🎯 Mural com alvo e trilhas de pegadas convergentes | OKR — Objetivo e Resultados-Chave (outcome vs output) |
| 🪖 Líder trocando chapéus de pedra conforme contexto | Liderança Situacional (diretivo, coach, facilitador, delegador) |
| 🗳️ Círculo de votação com pedras brilhantes e opacas | Autogestão e Decisão por Consenso (ADR, DACI) |
| 📋 Mural dividido em zonas com marcas pessoais | Alinhamento de Responsabilidades (RACI, catálogo de serviços) |

### Micro — Dinâmica e Competências (faixa inferior)

| Nicho da ilustração | Conceito técnico |
|---|---|
| 🌱 Trogloditas ao redor de fogueira com gestos de apresentação | Forming — Fase de Formação do Grupo (Tuckman) |
| ⚡ Ferramentas apontadas em direções opostas, tensão evidente | Storming — Fase de Conflito Produtivo (Tuckman) |
| 🤝 Alinhamento de ferramentas e mural de regras compartilhado | Norming — Fase de Acordo e Normas (Tuckman) |
| 🚀 Linha sincronizada passando pedras sem hesitação | Performing — Fase de Alta Performance e Flow (Tuckman) |
| 🔍 Dupla com lupa revisando e trocando papéis | Code Review e Pair Programming |
| 🧠 Mural de perfis com símbolos de competência por membro | Skills Matrix — Mapeamento de Competências |
| 📚 Lacuna no mural + troglodita buscando pedra de treinamento | Gap de Competências e Plano de Aprendizagem (PDI) |
