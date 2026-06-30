# A Caverna do Código — SOLID, Padrões e Boas Práticas na Idade da Pedra

Objeto educacional no formato **mapa-metáfora**: uma única ilustração de caverna pré-histórica em corte transversal (estilo "casa de boneca") onde **a própria figura é a interface**. Cada nicho da arte é um hotspot interativo que ensina um fundamento de bom código. A cena se divide em uma faixa **superior** — a tribo macro (SOLID, padrões criacionais, estruturais e comportamentais, e complexidade Big-O) — e uma faixa **inferior** — os detalhes micro (os cinco princípios SOLID um a um, Clean Code e 12-Factor App). Em vez de 12 caixas isoladas, o aluno aprende por **espaço e história**, vendo como os princípios e padrões se conectam. Voltado para devs juniores.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador — sem instalação, sem servidor, sem build. O arquivo `caverna-do-codigo.png` (a ilustração) precisa ficar na mesma pasta que o `index.html`. Clique em qualquer nicho da caverna, use a **legenda numerada** (rota acessível alternativa) ou o **Tour guiado** para uma visita automática pelos 12 conceitos.

### Realces entre conceitos

Ao abrir um conceito, a figura "acende" o subsistema: o nicho ativo ganha halo forte, os relacionados pulsam com contorno tracejado e o resto é atenuado. O modal traz a seção **🔗 Conecta-se com**, com uma nota explicando o laço e chips clicáveis que saltam entre conceitos — materializando, por exemplo, que SRP, OCP, LSP, ISP e DIP são justamente as cinco tábuas que o conselho SOLID resume.

### Acessibilidade

Hotspots são `<button>` com `aria-label`, navegáveis por Tab/Enter e com foco visível; a legenda numerada é a rota alternativa para quem não percebe as regiões sobre a arte; `Esc` fecha o modal; com o Tour ativo, `←`/`→` navegam manualmente; setas movem o foco entre nichos; e `prefers-reduced-motion` desliga as animações de pulso/halo.

## Mapeamento

### Faixa superior — A Tribo Macro (princípios e padrões)

| Região da ilustração | Conceito técnico |
|---|---|
| 🏛️ Conselho de cinco anciãos com tábuas | SOLID (os cinco princípios em visão geral) |
| 🏺 Oficina de moldes, recipiente único e construtor | Padrões criacionais (Factory, Singleton, Builder) |
| 🧩 Adaptador de osso, camadas de couro e alavanca-fachada | Padrões estruturais (Adapter, Decorator, Facade) |
| 🔥 Cartões de tática, tocha-sinal e roteiro em tábua | Padrões comportamentais (Strategy, Observer, Template Method) |
| ⏳ Escada, rampa em espiral e elevador de contrapeso | Complexidade Big-O (eficiência do caminho) |

### Faixa inferior — Os Detalhes Micro (práticas)

| Região da ilustração | Conceito técnico |
|---|---|
| 🔨 Ferramenta de função única e inequívoca | Single Responsibility Principle (SRP) |
| 🧱 Estrutura central com módulos encaixáveis | Open/Closed Principle (OCP) |
| 🔄 Troca da peça A pela B no mesmo slot | Liskov Substitution Principle (LSP) |
| 🎛️ Placas especializadas vs. placa sobrecarregada | Interface Segregation Principle (ISP) |
| 🪢 Alavanca puxando um mecanismo oculto por corda | Dependency Inversion Principle (DIP) |
| 🧼 Tábua de desenhos limpos sendo polida com um pano | Clean Code (clareza, DRY, funções curtas) |
| 🔐 Cofre de ossos com chave + pedras coloridas em pilha | 12-Factor App (configuração no ambiente, logs como eventos) |

## Créditos de design

Ilustração gerada a partir do prompt de "caverna pré-histórica em corte transversal, 12 nichos separados por pilares de rocha, sem nenhum texto queimado na arte". A imagem (`caverna-do-codigo.png`, proporção 16:9) acompanha o objeto. Para honrar a regra do projeto de **zero dependências externas**, as fontes usam uma stack serif do sistema — nenhuma requisição de rede é feita ao abrir o objeto.
