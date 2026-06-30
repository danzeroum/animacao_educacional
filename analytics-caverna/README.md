# A Tribo Analítica — Analytics e Tomada de Decisão na Idade da Pedra

Objeto educacional no formato **mapa-metáfora**: uma única ilustração de uma caverna pré-histórica em corte transversal onde **a própria figura é a interface**. Cada nicho da caverna é um hotspot interativo que ensina um conceito de analytics e tomada de decisão baseada em dados. A cena se divide em uma **Faixa Superior** (a tribo analítica: análise descritiva, inferência e teste de hipótese, regressão linear, amostragem, dashboard analítico) e uma **Faixa Inferior** (os detalhes micro: média, mediana, moda, desvio padrão, erro tipo I, erro tipo II, R²). Voltado para devs juniores que precisam entender analytics aplicado a produtos e negócios.

## Como usar

Abra o arquivo `index.html` diretamente no seu navegador — sem instalação, sem servidor, sem build. O arquivo `analytics-caverna.png` (a ilustração) precisa ficar na mesma pasta que o `index.html`. Clique em qualquer nicho da caverna, use a **legenda numerada** (rota acessível alternativa) ou o **Tour guiado** para uma visita automática pelos 12 conceitos.

### Realces entre conceitos

Ao abrir um conceito, a figura "acende" o sub-sistema: o setor ativo ganha halo forte, os conceitos relacionados pulsam com contorno tracejado e o resto é atenuado. O modal traz a seção **🔗 Conecta-se com**, com chips clicáveis que saltam entre os conceitos — mostrando como média, mediana e desvio compõem a análise descritiva, e como inferência depende de amostragem e controla erros tipo I/II.

### Acessibilidade

Hotspots são `<button>` com `aria-label`, navegáveis por Tab/Enter e com foco visível; a legenda numerada é a rota alternativa; `Esc` fecha o modal; com o Tour ativo, `←`/`→` navegam manualmente; e `prefers-reduced-motion` desliga as animações de pulso/halo.

## Mapeamento

### Faixa Superior — A Tribo Analítica (processo de decisão)

| Nicho da ilustração | Conceito técnico |
|---|---|
| 📊 Mural com representações de pedras e medidas | Análise Descritiva (estatísticas básicas, EDA) |
| ⚖️ Dois trogloditas debatendo mural H₀/H₁ | Inferência e Teste de Hipótese (p-valor, A/B testing) |
| 📐 Régua de pedra alinhando duas trilhas de pegadas | Regressão Linear (linha de melhor ajuste, correlação) |
| 🪣 Troglodita coletando pedras por métodos distintos | Amostragem (aleatória, estratificada, sistemática) |
| 🗂️ Sábio consultando painel com múltiplos indicadores | Dashboard Analítico (KPIs, data freshness, BI) |

### Faixa Inferior — Os Detalhes Micro (métricas e erros)

| Nicho da ilustração | Conceito técnico |
|---|---|
| ⚖️ Viga equilibrada sobre fulcro com pedras dos lados | Média (centro de gravidade, sensibilidade a outliers) |
| 🦴 Fileira ordenada com marcador de osso no centro | Mediana (robustez a outliers, p50) |
| 🏔️ Pilha de pedras idênticas que se destaca | Moda (frequência visual, dados categóricos) |
| 🎯 Círculo concêntrico em três camadas de dispersão | Desvio Padrão (±1σ, z-score, controle estatístico) |
| 🚨 Guardião rejeitando pedra válida | Erro Tipo I — Falso Positivo (α, múltiplos testes) |
| 🫥 Guardião aceitando pedra defeituosa | Erro Tipo II — Falso Negativo (β, poder estatístico) |
| 📏 Sábio comparando dois cenários de ajuste de régua | R² e Qualidade do Ajuste (overfitting, RMSE) |
