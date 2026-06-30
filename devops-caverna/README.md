# A Caverna DevOps — CI/CD, Observabilidade e Segurança na Idade da Pedra

Objeto educacional interativo no formato **mapa-metáfora** para devs juniores. Uma caverna pré-histórica em corte transversal (estilo "casa de boneca") vira a interface: a **faixa superior** é a *visão macro do pipeline DevOps* (a tribo automatizada — CI/CD, Observabilidade, DevSecOps, Microserviços e Rollback) e a **faixa inferior** são as *práticas e salvaguardas micro* (Build, Testes, Stage, Deploy, Logs, Métricas e SAMM). Cada nicho — separado por pilares de rocha — é um conceito de **DevOps e Engenharia de Software**. Clique em qualquer nicho para abrir a explicação, ou use o **tour guiado** para percorrer os 12 conceitos em ordem.

A ilustração de fundo é a arte `caverna-devops.png` (sem CDN); todo o CSS e JS são inline no `index.html`, que abre com duplo clique.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador. O arquivo `caverna-devops.png` precisa estar na mesma pasta.

- Clique em um nicho (ou use a legenda numerada / o tour guiado) para abrir o conceito.
- Teclado: `Tab` foca os nichos, `Enter` abre, `Esc` fecha; setas `←→` navegam no tour; setas `←→↑↓` navegam entre hotspots com modal fechado.

## Mapeamento

### Macro — A Tribo Automatizada (Faixa Superior)

| Elemento da caverna | Conceito técnico |
|---|---|
| 🔩 Esteira de madeira e corda com 4 estações sequenciais (Build, Test, Stage, Deploy) | **CI/CD Pipeline** — linha de montagem contínua com portões de aprovação |
| 🔭 Painel triplo de pedra com tambor de eventos, mural de gráficos e corda com nós coloridos | **Observabilidade** — os três pilares: Logs, Métricas e Tracing |
| 🛡️ Guardião com escudo e lupa presente em todas as estações do pipeline | **DevSecOps** — segurança integrada e deslocada para a esquerda |
| 🏛️ Compartimentos autônomos separados por pilares de rocha com pontes padronizadas | **Microserviços** — serviços independentes comunicando via contratos |
| ↩️ Mecanismo de contrapeso e alavanca de emergência com sensor de anomalia | **Rollback Automatizado** — reversão mecânica sem intervenção manual |

### Micro — As Práticas do Pipeline (Faixa Inferior)

| Elemento da caverna | Conceito técnico |
|---|---|
| 🔨 Artesão encaixando peças padronizadas com pilha de reservas ao lado | **Build** — montagem modular com artefatos reproduzíveis e imutáveis |
| 🔬 Três dispositivos de teste: martelo, fogueira controlada e rampa de desgaste | **Testes Automatizados** — pirâmide de testes, contract testing, cobertura |
| 🌧️ Área de simulação com chuva artificial, pouca luz e terreno irregular | **Stage** — validação em ambiente que espelha produção |
| 🚀 Calha distribuindo ferramenta aprovada para múltiplos compartimentos | **Deploy & Distribuição** — blue/green, canary, GitOps |
| 📋 Tambor de pedras com três marcas por pedra (origem, tipo, timestamp) | **Logs Estruturados** — registro com contexto para rastreio e filtragem |
| 📊 Mural com colunas em relevo e relógio de areia duplo (build vs. deploy) | **Métricas de Performance** — DORA metrics, SLOs, error budget |
| 🗿 Cinco pilares de rocha: Governança, Design, Implementação, Verificação, Operação | **SAMM** — Software Assurance Maturity Model nas 5 dimensões |
