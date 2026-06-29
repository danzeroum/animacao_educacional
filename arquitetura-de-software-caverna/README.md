# A Caverna Arquitetada — Arquitetura de Software na Idade da Pedra

Objeto educacional no formato **mapa-metáfora**: uma única ilustração coesa de uma caverna pré-histórica em corte transversal onde **a própria figura é a interface**. Cada região da arte é um hotspot interativo que ensina um conceito de arquitetura de software. A cena se divide em uma faixa **Macro** (a caverna-tribo: escalabilidade, segurança, DevOps, cloud, redundância) e uma faixa **Micro** (a parede de pinturas: C4, observabilidade, refatoração, leis, criptografia, conformidade, dívida técnica). Em vez de 12 caixas isoladas, o aluno aprende por **espaço e história** — vendo proximidade, fluxo e escala entre os conceitos. Voltado para devs juniores.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador — sem instalação, sem servidor, sem build. O arquivo `caverna-arquitetada-v2.png` (a ilustração) precisa ficar na mesma pasta que o `index.html`. Clique em qualquer setor da caverna, use a **legenda numerada** (rota acessível alternativa) ou o **Tour guiado** para uma visita automática pelos 12 conceitos.

### Realces Macro ↔ Micro (Fase 2)

Ao abrir um conceito, a figura "acende" o sub-sistema: o setor ativo ganha halo forte, os relacionados pulsam com contorno tracejado e o resto é atenuado. O modal traz a seção **🔗 Conecta-se com**, com uma nota explicando o laço e chips clicáveis que saltam entre os conceitos relacionados — materializando como uma decisão lá no macro reflete aqui no micro.

### Acessibilidade

Hotspots são `<button>` com `aria-label`, navegáveis por Tab/Enter e com foco visível; a legenda numerada é a rota alternativa para quem não percebe as regiões sobre a arte; `Esc` fecha o modal; com o Tour ativo, `←`/`→` navegam manualmente; e `prefers-reduced-motion` desliga as animações de pulso/halo.

## Mapeamento

### Macro — A Caverna-Tribo

| Região da ilustração | Conceito técnico |
|---|---|
| 🪨 Blocos de pedra sendo empilhados (esquerda) | Escalabilidade (expansão modular / horizontal) |
| 🛡️ Portão fortificado + espinhos de osso + crachá-pedra | Segurança (autenticação e autorização) |
| 🏹 Máquina de caça automática + vasos de argila | DevOps & CI/CD (testes automatizados, containers) |
| ☁️ Coluna de fumaça azul para cavernas distantes | Cloud (recursos sob demanda, coordenação remota) |
| 🔥 Duas fogueiras gêmeas (direita) | Disponibilidade & redundância (failover) |

### Micro — A Parede de Pinturas

| Região da ilustração | Conceito técnico |
|---|---|
| 🎨 Tábuas de pedra em camadas | Modelo C4 (Contexto → Container → Componente → Código) |
| 👣 Pegadas + corda de nós + fogueira de cor | Observabilidade (logging, tracing, monitoramento) |
| 🔨 Troglodita reconstruindo a ferramenta | Refatoração (redução de acoplamento) |
| ⚖️ Dois menires gravados (músculo / clima) | Leis da arquitetura (trade-offs e contexto) |
| 🦴 Cofre de ossos + chave-pedra | Criptografia & acesso mínimo (dados sensíveis) |
| 📜 Ancião entregando tábua a um jovem | Conformidade (LGPD / GDPR) |
| 💀 Pilha de ferramentas quebradas + sábio apontando | Dívida técnica |

## Créditos de design

Implementado a partir do pacote de handoff em [`design_handoff_caverna_figura/`](./design_handoff_caverna_figura/) (conceitos, posições de hotspot, relações Macro↔Micro e tokens). A ilustração `caverna-arquitetada-v2.png` (2752×1536, sem texto queimado) acompanha o bundle. Para honrar a regra do projeto de **zero dependências externas**, as fontes do protótipo (Cinzel/Spectral, via Google Fonts) foram substituídas por uma stack serif do sistema — nenhuma requisição de rede é feita ao abrir o objeto.
