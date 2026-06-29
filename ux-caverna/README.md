# A Caverna do UX — Experiência do Usuário na Idade da Pedra

Objeto educacional no formato **mapa-metáfora**: uma única ilustração coesa de uma caverna pré-histórica em corte transversal onde **a própria figura é a interface**. Cada nicho da arte é um hotspot interativo que ensina um conceito de **UX no desenvolvimento de software**. A cena se divide em uma faixa **Macro** (o processo de UX da tribo: empatia, avaliação heurística, prototipação, arquitetura da informação e teste de usabilidade) e uma faixa **Micro** (as heurísticas e práticas: facilidade de aprender, eficiência, retenção, prevenção de erros, recuperação de erros, satisfação e co-criação). Em vez de 12 caixas isoladas, o aluno aprende por **espaço e história** — vendo como cada decisão de design vive dentro da jornada de quem usa o produto. Voltado para devs juniores.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador — sem instalação, sem servidor, sem build. O arquivo `ux-caverna.png` (a ilustração) precisa ficar na mesma pasta que o `index.html`. Clique em qualquer nicho da caverna, use a **legenda numerada** (rota acessível alternativa) ou o **Tour guiado** para uma visita automática pelos 12 conceitos.

### Realces Processo ↔ Heurísticas

Ao abrir um conceito, a figura "acende" o sub-sistema: o nicho ativo ganha halo forte, os relacionados pulsam com contorno tracejado e o resto é atenuado. O modal traz a seção **🔗 Conecta-se com**, com uma nota explicando o laço e chips clicáveis que saltam entre os conceitos relacionados. O caso mais nítido: ao abrir a **Avaliação Heurística** (o conselho de anciãos), a figura acende as cinco heurísticas que cada ancião segura no andar de baixo — aprender, eficiência, retenção, prevenção de erros e satisfação.

### Acessibilidade

Hotspots são `<button>` com `aria-label`, navegáveis por Tab/Enter e com foco visível; a legenda numerada é a rota alternativa para quem não percebe as regiões sobre a arte; `Esc` fecha o modal; com o Tour ativo, `←`/`→` navegam manualmente; setas movem o foco entre hotspots; e `prefers-reduced-motion` desliga as animações de pulso/halo.

## Mapeamento

### Macro — O Processo de UX (a tribo trabalhando)

| Região da ilustração | Conceito de UX |
|---|---|
| 🫶 Troglodita observando outro usar a ferramenta + tábua de emoções | Empatia (pesquisa contextual, imersão no usuário) |
| 🔍 Conselho de anciãos circulando a interface de pedra com tábuas-heurística | Avaliação Heurística (inspeção contra as 10 de Nielsen) |
| ✏️ Grupo desenhando oito esboços numa mesa de argila | Prototipação Rápida (Crazy 8s, baixa fidelidade) |
| 🗺️ Mural de cavernas aninhadas + trilhas de pegadas + símbolos sobre entradas | Arquitetura da Informação (hierarquia, navegação, rotulagem) |
| 👀 Usuário buscando uma ferramenta + observadores atrás da fenda | Teste de Usabilidade (observação moderada, tarefas reais) |

### Micro — Heurísticas & Práticas (as paredes de prática)

| Região da ilustração | Conceito de UX |
|---|---|
| 🧑‍🏫 Jovem aprendendo com guia de pedra de 3 passos | Facilidade de Aprender (learnability, onboarding) |
| ⚡ Caminho direto vs. labirinto tortuoso | Eficiência (caminho ótimo, aceleradores) |
| 🧠 Troglodita retornando com nuvem de memória do fluxo | Retenção / Memorabilidade (consistência) |
| 🚫 Mecanismo de encaixe exclusivo bloqueando a ferramenta errada | Prevenção de Erros (design à prova de falhas) |
| ↩️ Alavanca de reverter + caixa de reparo acessível | Recuperação de Erros (undo, mensagens úteis) |
| 😊 Troglodita sorrindo com ferramenta ergonômica | Satisfação & Delight (prazer de uso) |
| 🤝 Círculo desenhando e trocando tábuas | Co-criação (workshops, design colaborativo) |

## Créditos de design

A ilustração `ux-caverna.png` (cartoon pré-histórico, corte transversal, 16:9, sem texto queimado) foi gerada a partir do prompt editorial de "UX no Desenvolvimento de Software" e acompanha este objeto. Para honrar a regra do projeto de **zero dependências externas**, as fontes evocadas (Cinzel/Spectral) usam uma stack serif do sistema — nenhuma requisição de rede é feita ao abrir o objeto.
