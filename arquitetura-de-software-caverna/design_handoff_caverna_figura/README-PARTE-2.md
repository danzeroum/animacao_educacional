# Handoff (Parte 2): Conteúdo, Modal, Interações e Tokens

> Os textos completos dos 12 conceitos (metáfora, bullets, ferramentas, dica) estão
> **verbatim** no arquivo do protótipo incluído neste bundle:
> `Caverna Arquitetada — Figura Interligada.dc.html`, no objeto `CONCEITOS` da classe
> lógica. Copie-os de lá — são longos e já revisados. Abaixo está a **estrutura** de
> cada registro, a lista de chaves, cores e ícones, e o mapa de relações da Fase 2.

## Estrutura de cada conceito (`CONCEITOS[chave]`)
```js
{
  zona:        "Macro · A Caverna-Tribo" | "Micro · A Parede de Pinturas",
  titulo:      "Escalabilidade — O Abrigo que Cresce",   // título do modal
  icone:       "🪨",                                       // emoji (só no modal)
  cor:         "#d9a441",                                  // cor-tema do conceito
  label:       "Escalabilidade",                           // rótulo curto (legenda/chip)
  metafora:    "texto em itálico, a história pré-histórica do conceito",
  bullets:     ["3 pontos técnicos que traduzem a metáfora para a prática", ...],
  ferramentas: [ {nome:"Kubernetes", url:"https://kubernetes.io"}, ... ],  // 3 links reais
  dica:        "💡 Dica de Arquiteto — um conselho prático acionável"
}
```

## As 12 chaves, cor-tema, ícone e zona
| chave | label | cor | ícone | zona |
|---|---|---|---|---|
| `escalabilidade` | Escalabilidade | `#d9a441` | 🪨 | Macro |
| `seguranca` | Segurança | `#c0563a` | 🛡️ | Macro |
| `devops` | DevOps & CI/CD | `#6ba368` | 🏹 | Macro |
| `cloud` | Cloud | `#8fb8d6` | ☁️ | Macro |
| `redundancia` | Disponibilidade & Redundância | `#ff7a18` | 🔥 | Macro |
| `c4` | Modelo C4 | `#d4915a` | 🎨 | Micro |
| `observabilidade` | Observabilidade | `#5fc8a0` | 👣 | Micro |
| `refatoracao` | Refatoração | `#c9aa5c` | 🔨 | Micro |
| `leis` | Leis da Arquitetura | `#b08cc4` | ⚖️ | Micro |
| `cofre` | Cofre de Ossos | `#cdbd9a` | 🦴 | Micro |
| `conformidade` | Conformidade | `#e0c04a` | 📜 | Micro |
| `divida` | Dívida Técnica | `#9aa0a6` | 💀 | Micro |

A ordem de exibição (numeração 1–12 na legenda e no Tour) segue exatamente a tabela
acima.

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
Overlay fixo cobrindo a tela, fundo `rgba(8,5,2,.8)` + `backdrop-filter: blur(3px)`,
centralizado. Card branco-pergaminho. Fecha por: botão ✕, clique no overlay, ou `Esc`.

**Card:** `background:#f4ecde; border-radius:16px; padding:24px; max-width:540px;
width:100%; max-height:88vh; overflow-y:auto; border-top:6px solid <cor-do-conceito>;
box-shadow:0 30px 80px -20px rgba(0,0,0,.7)`. Entra com animação `cvslide` (sobe 18px
+ fade, .26s ease).

**Conteúdo, de cima para baixo:**
1. Header: ícone (34px) + zona (kicker, `#9a7b4a`, uppercase, letter-spacing .18em) +
   título (`Cinzel` 700, 21px, `#2a2018`) + botão ✕ (34×34, `#2a2018`).
2. Metáfora: itálico, `#5a4633`, 14.5px, `border-left:3px solid <cor>`, padding-left 14.
3. Bullets: lista sem marcador; cada item com um ponto `<cor>` (7px) à esquerda;
   texto `#3a2e22`, 14px.
4. Ferramentas reais: rótulo "Ferramentas reais" + chips-link (`<a target="_blank">`),
   `background:#f3e4c4; border:1px solid #cdab6b; color:#6b4a17; border-radius:7px`.
5. **🔗 Conecta-se com** (Fase 2): nota em itálico + chips clicáveis dos relacionados.
   Cada chip: `border-left:4px solid <cor-do-relacionado>;
   background: color-mix(in srgb, <cor> 22%, #f3e4c4)`; ícone + label; ao clicar,
   abre o conceito relacionado (troca o conteúdo do modal sem fechar).
6. Dica de Arquiteto: bloco `background:#f3e4c4; border-left:4px solid <cor>`, título
   "💡 Dica de Arquiteto" (`Cinzel`, `#7a4f00`) + texto `#5a3d0a`.

## Marcadores na figura (hotspot, estados)
- **Repouso:** ponto central (11px, cor do conceito, `box-shadow:0 0 10px <cor>`),
  animação `cvpulse` 2.4s (escala 1→1.55, opacidade 0.85→0.35), mais um anel
  `cvring` 2.4s (escala 0.6→2.4, fade-out). Um estilo alternativo "Números" mostra um
  disco numerado no lugar do ponto.
- **Hover:** no botão, `border-color:<cor>; background: color-mix(in srgb,<cor> 15%,
  transparent); box-shadow:0 0 30px 2px color-mix(in srgb,<cor> 60%,transparent)`.
- **Ativo (Fase 2):** halo forte — `inset:-3px; border:3px solid <cor>;
  box-shadow:0 0 34px 4px <cor>, inset 0 0 22px ...; background:<cor> a 14%`.
- **Relacionado (Fase 2):** `border:2px dashed <cor>; box-shadow:0 0 20px <cor>;
  animation:cvhalo 1.8s` (opacidade pulsa 0.45→1).
- **Atenuado (Fase 2):** marcadores dos não-relacionados caem para `opacity:.28–.3`.

## Interações & comportamento
- **Hotspot / legenda / chip** → abre o modal do conceito.
- **Tour guiado** (botão): percorre os 12 conceitos em sequência, avançando sozinho a
  cada 4.2s; setas ←/→ navegam manualmente; abre cada modal e destaca a figura.
- **Teclado:** `Esc` fecha; `←`/`→` navegam o tour quando ativo. Hotspots são
  `<button>` (Tab/Enter, foco visível). A legenda numerada é a rota acessível
  alternativa para quem não percebe as regiões sobre a arte.
- **prefers-reduced-motion:** desliga `cvpulse`, `cvring`, `cvhalo` (sem flicker).

## Estado necessário
- `activeId` — chave do conceito aberto (ou null). Controla modal + halos.
- `tourActive` / `tourIdx` — controle do tour automático (+ `setInterval`).
- Não há fetch de dados: tudo é estático (`CONCEITOS`, `RELACOES`, `GEO`).

## Design tokens
**Cores de chrome:** fundo caverna `#160e07`/`#100a05`/`#2a1c10`; cards escuros
`#1d140c`–`#221a0e`; bordas `#3a2c1e`/`#6d5b47`; dourado de destaque `#f0d29a`,
`#e0b066`, `#b9925a`; texto claro `#f0e6d2`/`#d9c4a0`/`#cdbb9a`. Pergaminho do modal
`#f4ecde`/`#f3e4c4`. **Cores dos conceitos:** ver tabela na Parte 2.
**Tipografia:** títulos `Cinzel` (serif display, 500/600/700); corpo `Spectral`
(serif, 400/500/600 + itálico). Importadas do Google Fonts.
**Raios:** cards 14px, figura/modal 16px, chips 6–8px. **Animações:** `cvpulse`,
`cvring`, `cvhalo`, `cvslide` (definições no `<style>` do protótipo).

## Assets
- `caverna-arquitetada-v2.png` (2752×1536, 16:9) — a ilustração principal, **sem
  texto queimado**. Incluída neste bundle. Foi gerada por IA a partir do prompt
  documentado pela equipe de design; se precisar regenerar, mantenha a regra "nenhuma
  letra/número legível; gravuras = símbolos rupestres abstratos" e a ordem espacial
  dos 12 setores (esquerda→direita, macro em cima / micro embaixo) para reaproveitar
  as posições de hotspot.
- Emojis dos ícones de conceito: usados apenas dentro do modal (não sobre a arte).

## Files
- `Caverna Arquitetada — Figura Interligada.dc.html` — protótipo funcional completo
  (fonte de verdade para textos, cores, posições e comportamento).
- `caverna-arquitetada-v2.png` — ilustração.
- `README.md` (Parte 1) — visão geral, layout, figura e posições dos hotspots.
- `README-PARTE-2.md` (este arquivo) — conteúdo, modal, interações, tokens, estado.
