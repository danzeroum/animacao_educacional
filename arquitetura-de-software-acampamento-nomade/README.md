# O Acampamento Arquitetado — Arquitetura de Software no Acampamento Nômade

Objeto educacional no formato **mapa-metáfora**: uma única ilustração coesa de um acampamento de caravana nômade no deserto em corte transversal (estilo "casa de boneca") onde **a própria figura é a interface**. Cada nicho da arte é um hotspot interativo que ensina um conceito de arquitetura de software. A cena se divide em uma faixa **Macro** (o acampamento e a rota migratória, ao ar livre: escalabilidade, segurança, DevOps, cloud, redundância) e uma faixa **Micro** (dentro da tenda do guia, o centro de controle: C4, observabilidade, refatoração, leis, criptografia, conformidade, dívida técnica). Em vez de 12 caixas isoladas, o aluno aprende por **espaço e história** — vendo proximidade, fluxo e escala entre os conceitos. Voltado para devs juniores.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador — sem instalação, sem servidor, sem build. O arquivo `acampamento-nomade.png` (a ilustração, 2752×1536) precisa ficar na mesma pasta que o `index.html`. Clique em qualquer nicho do acampamento, use a **legenda numerada** (rota acessível alternativa) ou o **Tour guiado** para uma visita automática pelos 12 conceitos.

> **Nota sobre a ilustração:** o `index.html` referencia `acampamento-nomade.png`. Coloque o PNG renderizado (proporção 2752×1536 ≈ 16:9, sem texto queimado) nesta pasta. Sem o arquivo, os hotspots, a legenda e o tour continuam funcionando, mas o fundo da figura aparece vazio. As posições dos hotspots (`GEO`, no `index.html`) foram estimadas a partir do layout dos 12 nichos e podem ser afinadas ao PNG final.

### Realces Macro ↔ Micro

Ao abrir um conceito, a figura "acende" o sub-sistema: o nicho ativo ganha halo forte, os relacionados pulsam com contorno tracejado e o resto é atenuado. O modal traz a seção **🔗 Conecta-se com**, com uma nota explicando o laço e chips clicáveis que saltam entre os conceitos relacionados — materializando como uma decisão lá no macro reflete aqui no micro.

### Acessibilidade

Hotspots são `<button>` com `aria-label`, navegáveis por Tab/Enter e com foco visível; a legenda numerada é a rota alternativa para quem não percebe os nichos sobre a arte; `Esc` fecha o modal; as setas `←`/`→`/`↑`/`↓` movem o foco entre os nichos (e navegam o Tour quando ativo); e `prefers-reduced-motion` desliga as animações de pulso/halo.

## Mapeamento

### Macro — O Acampamento e a Rota (ao ar livre)

| Elemento da ilustração | Conceito técnico |
|---|---|
| ⛺ Nômades montando novas tendas idênticas ligadas por passarelas | Escalabilidade (somar instâncias iguais / horizontal) |
| 🛡️ Paliçada de madeira, vigias com tochas e armadilha de ossos no portão | Segurança (autenticação e autorização) |
| 📦 Desmontar/montar tendas + sacos de carga idênticos enfileirados no boi | DevOps & CI/CD (testes automatizados, containers) |
| 🌟 Constelação-guia única com raios de luz azul ramificando | Cloud (referência remota compartilhada, sob demanda) |
| 💧 Dois poços gêmeos idênticos em pontos separados | Disponibilidade & redundância (failover) |

### Micro — Dentro da Tenda do Guia

| Elemento da ilustração | Conceito técnico |
|---|---|
| 🗺️ Quatro pergaminhos de couro sobrepostos (rota → objeto) | Modelo C4 (Contexto → Container → Componente → Código) |
| 🏮 Cordão de nós coloridos + trilha de pegadas + lanterna que muda de cor | Observabilidade (logging, tracing, monitoramento) |
| 🔧 Nômade trocando ferramentas pesadas por peças modulares encaixáveis | Refatoração (redução de acoplamento) |
| ⚖️ Dois totens de madeira gravados (pegada pesada; montanha sob o sol) | Leis da arquitetura (trade-offs e contexto) |
| 🔑 Baú trancado com símbolo tribal + chave de ossos única | Criptografia & acesso mínimo (dados sensíveis) |
| 📜 Ancião entregando um rolo de pergaminho a um jovem | Conformidade & tradições (LGPD / GDPR, padrões herdados) |
| 🎒 Fardo pesado transbordando pedras inúteis e ferramentas quebradas | Dívida técnica |

## Créditos de design

Terceiro objeto da série **Arquitetura de Software** (ao lado de [`arquitetura-de-software-caverna/`](../arquitetura-de-software-caverna/) e [`arquitetura-software-aldeia/`](../arquitetura-software-aldeia/)), aqui sob a metáfora do **acampamento nômade / caravana no deserto**. Para honrar a regra do projeto de **zero dependências externas**, as fontes usam uma stack serif do sistema (Bitter/Spectral → Georgia → serif) — nenhuma requisição de rede é feita ao abrir o objeto. A única origem local é a própria ilustração `acampamento-nomade.png`.
