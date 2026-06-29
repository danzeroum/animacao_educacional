# Handoff (Parte 2): Conteúdo, Modal, Interações e Tokens

> Os textos completos dos 12 conceitos (metáfora, bullets, ferramentas, dica) estão
> **verbatim** no arquivo do protótipo incluído neste bundle:
> `Aldeia Arquitetada - Figura Interligada.dc.html`, no objeto `CONCEITOS` da classe
> lógica. Copie-os de lá — são longos e já revisados. Abaixo está a **estrutura** de
> cada registro, a lista de chaves, cores e ícones, e o mapa de relações da Fase 2.

## Estrutura de cada conceito (`CONCEITOS[chave]`)
```js
{
  zona:        "Macro · A Aldeia" | "Micro · Dentro do Celeiro",
  titulo:      "Escalabilidade — A Horta que Cresce em Leiras",  // título do modal
  icone:       "🌱",                                              // emoji (só no modal)
  cor:         "#6f9b3f",                                         // cor-tema do conceito
  label:       "Escalabilidade",                                  // rótulo curto (legenda/chip)
  metafora:    "texto em itálico, a história rural do conceito",
  bullets:     ["3 pontos técnicos que traduzem a metáfora para a prática", ...],
  ferramentas: [ {nome:"Kubernetes", url:"https://kubernetes.io"}, ... ],  // 3 links reais
  dica:        "💡 Dica de Arquiteto — um conselho prático acionável"
}
```

## As 12 chaves, cor-tema, ícone e zona
| chave | label | cor | ícone | zona |
|---|---|---|---|---|
| `escalabilidade` | Escalabilidade | `#6f9b3f` | 🌱 | Macro |
| `seguranca` | Segurança | `#a85b32` | 🛡️ | Macro |
| `devops` | DevOps & CI/CD | `#c79a3b` | 🌾 | Macro |
| `cloud` | Cloud | `#5b9bc4` | ☁️ | Macro |
| `redundancia` | Disponibilidade & Redundância | `#c2792e` | 🌿 | Macro |
| `c4` | Modelo C4 | `#8a6d3f` | 🗺️ | Micro |
| `observabilidade` | Observabilidade | `#4f9e7a` | 🏮 | Micro |
| `refatoracao` | Refatoração | `#b07a3a` | 🔨 | Micro |
| `leis` | Leis da Arquitetura | `#9a6fb0` | ⚖️ | Micro |
| `cofre` | Baú de Sementes | `#7a8a4a` | 🔑 | Micro |
| `conformidade` | Conformidade | `#d2a93a` | 📜 | Micro |
| `divida` | Dívida Técnica | `#9a8466` | 🪓 | Micro |

A ordem de exibição (numeração 1–12 na legenda e no Tour) segue exatamente a tabela
acima — a mesma ordem espacial esquerda→direita, macro em cima / micro embaixo.

> Nota: o **conteúdo técnico** de cada conceito é idêntico ao da versão "caverna";
> apenas as **metáforas narrativas** (e os ícones/cores rurais) mudaram. Ex.: "lajes"
> → "leiras", "fogueiras gêmeas" → "hortas gêmeas", "sinais de fumaça" →
> "reservatório-nuvem + canais de água", "cofre de ossos" → "baú de sementes".

## Fase 2 — Mapa de relações (Macro ↔ Micro)
Ao abrir um conceito, destacam-se os relacionados. `RELACOES[chave] = { ids:[...],
nota:"frase que explica o laço" }`. As notas completas estão no protótipo; os laços:
- `escalabilidade` → cloud, redundancia, devops
- `seguranca` → cofre, conformidade, redundancia
- `devops` → escalabilidade, observabilidade, cloud
- `cloud` → escalabilidade, redundancia, conformidade
- `redundancia` → escalabilidade, observabilidade, seguranca
- `c4` → leis, observabilidade, refatoracao
- `observabilidade` → devops, redundancia, divida
- `refatoracao` → divida, leis, c4
- `leis` → c4, refatoracao, divida
- `cofre` → seguranca, conformidade
- `conformidade` → seguranca, cofre, cloud
- `divida` → refatoracao, observabilidade, leis

## O MODAL (ao clicar num hotspot ou chip)
Overlay fixo cobrindo a tela, fundo `rgba(40,28,12,.72)` + `backdrop-filter: blur(3px)`,
centralizado. Card pergaminho claro. Fecha por: botão ✕, clique no overlay, ou `Esc`.

**Card:** `background:#f6eece; border-radius:16px; padding:24px; max-width:540px;
width:100%; max-height:88vh; overflow-y:auto; border-top:6px solid <cor-do-conceito>;
box-shadow:0 30px 80px -20px rgba(40,28,12,.6)`. Entra com animação `alslide` (sobe
18px + fade, .26s ease).

**Conteúdo, de cima para baixo:**
1. Header: ícone (34px) + zona (kicker, `#9a7b4a`, uppercase, letter-spacing .16em) +
   título (`Bitter` 700, 21px, `#2f2616`) + botão ✕ (34×34, `#2f2616`).
2. Metáfora: itálico, `#5a4633`, 14.5px, `border-left:3px solid <cor>`, padding-left 14.
3. Bullets: lista sem marcador; cada item com um ponto `<cor>` (7px) à esquerda;
   texto `#3f3322`, 14px.
4. Ferramentas reais: rótulo "Ferramentas reais" + chips-link (`<a target="_blank">`),
   `background:#f3e4c4; border:1px solid #cdab6b; color:#6b4a17; border-radius:7px`.
5. **🔗 Conecta-se com** (Fase 2): nota em itálico + chips clicáveis dos relacionados.
   Cada chip: `border-left:4px solid <cor-do-relacionado>;
   background: color-mix(in srgb, <cor> 22%, #f3e4c4)`; ícone + label; ao clicar,
   abre o conceito relacionado (troca o conteúdo do modal sem fechar).
6. Dica de Arquiteto: bloco `background:#f3e4c4; border-left:4px solid <cor>`, título
   "💡 Dica de Arquiteto" (`Bitter`, `#7a4f00`) + texto `#5a3d0a`.

## Marcadores na figura (hotspot, estados)
Há 3 estilos de marcador de repouso, controlados por uma prop (`estiloMarcador`):
**"Números"** (padrão — disco numerado 1–12), **"Pontos pulsantes"** (ponto + anel) e
**"Nenhum"** (só hover, sem affordance permanente).
- **Repouso "Números":** disco 26px, `background:<cor>; color:#fff; font-family:Bitter
  700`, `box-shadow:0 0 0 3px rgba(60,46,28,.5),0 2px 8px rgba(0,0,0,.4)`.
- **Repouso "Pontos pulsantes":** ponto central (11px, cor do conceito,
  `box-shadow:0 0 10px <cor>`), animação `alpulse` 2.4s (escala 1→1.55, opacidade
  0.85→0.35), mais um anel `alring` 2.4s (escala 0.6→2.4, fade-out).
- **Hover:** no botão, `border-color:<cor>; background: color-mix(in srgb,<cor> 16%,
  transparent); box-shadow:0 0 30px 2px color-mix(in srgb,<cor> 60%,transparent)`.
- **Ativo (Fase 2):** halo forte — `inset:-3px; border:3px solid <cor>;
  box-shadow:0 0 34px 4px <cor>, inset 0 0 22px ...; background:<cor> a 14%`.
- **Relacionado (Fase 2):** `border:2px dashed <cor>; box-shadow:0 0 20px <cor>;
  animation:alhalo 1.8s` (opacidade pulsa 0.45→1).
- **Atenuado (Fase 2):** marcadores dos não-relacionados caem para `opacity:.3`.

## Interações & comportamento
- **Hotspot / legenda / chip** → abre o modal do conceito.
- **Tour guiado** (botão): percorre os 12 conceitos em sequência, avançando sozinho a
  cada 4.2s; setas ←/→ navegam manualmente; abre cada modal e destaca a figura.
- **Teclado:** `Esc` fecha; `←`/`→` navegam o tour quando ativo. Hotspots são
  `<button>` (Tab/Enter, foco visível). A legenda numerada é a rota acessível
  alternativa para quem não percebe as regiões sobre a arte.
- **prefers-reduced-motion:** desliga `alpulse`, `alring`, `alhalo` (sem flicker).

## Estado necessário
- `activeId` — chave do conceito aberto (ou null). Controla modal + halos.
- `tourActive` / `tourIdx` — controle do tour automático (+ `setInterval`).
- Não há fetch de dados: tudo é estático (`CONCEITOS`, `RELACOES`, `GEO`).

## Design tokens
**Cores de chrome (tema rural, fundo claro):** fundo campo
`#f4ecd6`/`#ecdfc0`/`#e2d2af`; cards claros `#f1e6cc`/`#f6eece`; bordas
`#d3bd8d`/`#b89255`; marrom de madeira `#6b4a2a`; títulos `#5a3d1c`; dourado de
destaque `#8a5a1e`/`#9a7434`; texto `#3c2e1c`/`#6f5a3c`/`#5c482e`. Pergaminho do
modal `#f6eece`/`#f3e4c4`. **Azul (#5b9bc4) é reservado só ao conceito `cloud`** (a
água) — não use azul em mais nenhum lugar do chrome. **Cores dos conceitos:** ver
tabela acima.
**Tipografia:** títulos `Bitter` (slab serif, 500/600/700); corpo `Spectral` (serif,
400/500/600 + itálico). Importadas do Google Fonts.
**Raios:** cards 14px, figura/modal 16px, chips 6–8px. **Animações:** `alpulse`,
`alring`, `alhalo`, `alslide` (definições no `<style>` do protótipo, dentro de
`<helmet>`).

## Props/tweaks do protótipo (traduzir como achar melhor)
- `estiloMarcador` (enum: "Pontos pulsantes" | "Números" | "Nenhum", default
  "Números") — estilo do marcador de repouso na figura.
- `mostrarPainelDev` (boolean, default true no protótipo) — liga o painel "Orientações
  para o Dev". **No objeto final do aluno deve ser `false`/removido** (ver aviso na
  Parte 1).

## Assets
- `aldeia-arquitetada.png` (2752×1536, 16:9) — a ilustração principal, **sem texto
  queimado**. Incluída neste bundle. Foi gerada por IA a partir de um prompt
  documentado pela equipe de design; se precisar regenerar, mantenha a regra "nenhuma
  letra/número legível; gravuras das tábuas = símbolos rurais abstratos (espigas, sol,
  gotas), jamais caracteres de alfabeto" e a ordem espacial dos 12 nichos
  (esquerda→direita, macro em cima / micro embaixo) para reaproveitar as posições de
  hotspot.
- Emojis dos ícones de conceito: usados apenas dentro do modal (não sobre a arte).

## Files
- `Aldeia Arquitetada - Figura Interligada.dc.html` — protótipo funcional completo
  (fonte de verdade para textos, cores, posições e comportamento).
- `aldeia-arquitetada.png` — ilustração.
- `README.md` (Parte 1) — visão geral, aviso de remoção do andaime, layout, figura e
  posições dos hotspots.
- `README-PARTE-2.md` (este arquivo) — conteúdo, modal, interações, tokens, estado.
