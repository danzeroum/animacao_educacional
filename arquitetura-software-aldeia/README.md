# A Aldeia Arquitetada — Arquitetura de Software na Aldeia Agrícola

Objeto educacional no formato **mapa-metáfora**: uma única ilustração coesa de uma aldeia agrícola em corte transversal (estilo "casa de boneca") onde **a própria figura é a interface**. Cada nicho da arte é um hotspot interativo que ensina um conceito de arquitetura de software. A cena se divide em uma faixa **Macro** (a aldeia ao ar livre: escalabilidade, segurança, DevOps, cloud, redundância) e uma faixa **Micro** (dentro do celeiro: C4, observabilidade, refatoração, leis, criptografia, conformidade, dívida técnica). Em vez de 12 caixas isoladas, o aluno aprende por **espaço e história** — vendo proximidade, fluxo e escala entre os conceitos. Voltado para devs juniores.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador — sem instalação, sem servidor, sem build. O arquivo `aldeia-arquitetada.png` (a ilustração) precisa ficar na mesma pasta que o `index.html`. Clique em qualquer nicho da aldeia, use a **legenda numerada** (rota acessível alternativa) ou o **Tour guiado** para uma visita automática pelos 12 conceitos.

### Realces Macro ↔ Micro (Fase 2)

Ao abrir um conceito, a figura "acende" o sub-sistema: o nicho ativo ganha halo forte, os relacionados pulsam com contorno tracejado e o resto é atenuado. O modal traz a seção **🔗 Conecta-se com**, com uma nota explicando o laço e chips clicáveis que saltam entre os conceitos relacionados — materializando como uma decisão lá no macro reflete aqui no micro.

### Acessibilidade

Hotspots são `<button>` com `aria-label`, navegáveis por Tab/Enter e com foco visível; a legenda numerada é a rota alternativa para quem não percebe os nichos sobre a arte; `Esc` fecha o modal; as setas `←`/`→`/`↑`/`↓` movem o foco entre os nichos (e navegam o Tour quando ativo); e `prefers-reduced-motion` desliga as animações de pulso/halo.

## Mapeamento

### Macro — A Aldeia (ao ar livre)

| Elemento da ilustração | Conceito técnico |
|---|---|
| 🌱 Agricultores arando e irrigando novas leiras (esquerda) | Escalabilidade (somar canteiros iguais / horizontal) |
| 🛡️ Celeiro com cerca dupla, portão e fechadura + guardião | Segurança (autenticação e autorização) |
| 🌾 Debulhadora automática + sacas/silos enfileirados + carro de boi | DevOps & CI/CD (testes automatizados, containers) |
| ☁️ Reservatório-nuvem + canais de água ramificando | Cloud (recursos sob demanda, distribuídos) |
| 🌿 Duas hortas gêmeas espelhadas (direita) | Disponibilidade & redundância (failover) |

### Micro — Dentro do Celeiro

| Elemento da ilustração | Conceito técnico |
|---|---|
| 🗺️ Painéis/mapas de madeira em camadas | Modelo C4 (Contexto → Container → Componente → Código) |
| 🏮 Mural com pegadas + corda de nós coloridos + lanterna | Observabilidade (logging, tracing, monitoramento) |
| 🔨 Agricultor reconstruindo o arado | Refatoração (redução de acoplamento) |
| ⚖️ Duas tábuas gravadas verticais | Leis da arquitetura (trade-offs e contexto) |
| 🔑 Baú de sementes trancado + chave única | Criptografia & acesso mínimo (dados sensíveis) |
| 📜 Ancião entregando rolo de regras a um jovem | Conformidade (LGPD / GDPR) |
| 🪓 Pilha de ferramentas enferrujadas + agricultor preocupado | Dívida técnica |

## Créditos de design

Implementado a partir do pacote de handoff em [`design_handoff_aldeia_figura/`](./design_handoff_aldeia_figura/) (conceitos, posições de hotspot, relações Macro↔Micro e tokens). A ilustração `aldeia-arquitetada.png` (2752×1536, sem texto queimado) acompanha o bundle. Para honrar a regra do projeto de **zero dependências externas**, as fontes do protótipo (Bitter/Spectral, via Google Fonts) foram substituídas por uma stack serif do sistema — nenhuma requisição de rede é feita ao abrir o objeto.
