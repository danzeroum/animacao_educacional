# A Caverna dos Processos — Automação & Orquestração (BPM/BPMS) na Idade da Pedra

Objeto educacional interativo no formato **mapa-metáfora** para devs juniores. Uma caverna pré-histórica em corte transversal (estilo "casa de boneca") vira a interface: a **faixa superior** é a *visão macro do processo* (a tribo desenha, decide, coordena e automatiza) e a **faixa inferior** são os *componentes e práticas micro*. Cada nicho — separado por pilares de rocha — é um conceito de **BPM / BPMS** (BPMN, gateways, DMN, process mining, orquestração, low-code, subprocessos, mensageria, retry/fallback, bots/RPA, monitoramento e automação end-to-end). Clique em qualquer nicho para abrir a explicação, ou use o **tour guiado** para percorrer os 12 conceitos em ordem.

A ilustração de fundo é a arte `caverna-processos.png` (sem CDN); todo o CSS e JS são inline no `index.html`, que abre por duplo clique.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador.

- Clique em um nicho (ou use a legenda numerada / o tour guiado) para abrir o conceito.
- Teclado: `Tab` foca os nichos, `Enter` abre, `Esc` fecha; setas `←→↑↓` navegam entre nichos e avançam/voltam no tour.

## Mapeamento

| Elemento da caverna | Conceito técnico |
|---|---|
| Tábua de pedra com raias e peças geométricas (círculo, retângulo, losango) | **BPMN** — modelagem visual de workflow |
| Portal de rocha com três passagens (barreira única, portas independentes, duas alavancas) | **Gateways XOR / OR / AND** — lógica de decisão |
| Mesa-tabuleiro com pedras coloridas em células de condição e resultado | **DMN** — tabelas de decisão |
| Duas trilhas de pegadas: a reta documentada e a tortuosa real; ancião analisando | **Process Mining** — processo real vs. documentado |
| Tambor central com cordas, roldanas, cestas-buffer e fumaça azul | **Orquestração BPMS** — automação coordenada |
| Peças de pedra com encaixes universais (tipo LEGO) montadas sobre argila | **Low-Code** — peças modulares de processo |
| Tábua de pedra contendo uma mini-tábua com outro fluxo | **Subprocessos aninhados** |
| Cestas idênticas deslizando num varal sobre a ravina entre dois grupos | **Acoplamento fraco** — REST API / mensageria |
| Corda principal que arrebenta e corda reserva assumindo o contrapeso | **Tolerância a falhas** — retry e fallback |
| Braço articulado de madeira com mola e ampulheta marcando o ritmo | **Digital Workers / Bots** (RPA) |
| Painel de pedra com pedras coloridas subindo por roldanas (níveis/gargalos) | **Monitoramento e dashboards** |
| Bola de pedra percorrendo a trilha inteira por rampas e portões temporizados; símbolo ∞ | **Automação End-to-End** |
