"""Templates de prompt do pipeline (contrato da imagem + objeto-como-JSON)."""
from __future__ import annotations

# ── Etapa 1: prompt da imagem (contrato de composição — PIPELINE.md §1/§4.3) ──
CONTRATO_IMAGEM = """\
Você é um diretor de arte. Gere a DESCRIÇÃO (prompt) de uma única ilustração de \
fundo para um objeto educacional no formato mapa-metáfora, tema "{tema}" com a \
metáfora "{metafora}".

Regras OBRIGATÓRIAS de composição:
- Proporção 16:9, preenchendo de borda a borda.
- DUAS FAIXAS horizontais: 5 nichos na faixa de cima, 7 nichos na de baixo (12 no total).
- Os nichos são separados por PILARES / COLUNAS de rocha — cada conceito no seu compartimento.
- SEM TEXTO e sem números: apenas símbolos/elementos visuais abstratos da metáfora.
- Estética coerente com a metáfora "{metafora}"; paleta sóbria, alto contraste entre nichos.

Responda APENAS com o texto do prompt de imagem (sem comentários, sem aspas)."""


# ── Etapa 3: objeto como JSON (A1 — nunca o HTML inteiro) ──
OBJETO_JSON = """\
Você cria objetos educacionais para devs juniores. Gere o CONTEÚDO de um objeto \
mapa-metáfora sobre "{tema}" usando a metáfora "{metafora}".

IMPORTANTE: EMITA APENAS UM JSON VÁLIDO (sem markdown, sem ```), no schema abaixo.
NÃO gere HTML — o HTML é montado por um template fixo a partir deste JSON.

São EXATAMENTE {n} conceitos. A imagem de fundo tem 5 nichos em cima e 7 embaixo,
separados por pilares; a geometria GEO posiciona cada hotspot sobre seu nicho.

Schema:
{{
  "metadados": {{
    "titulo": "Título curto do objeto",
    "titulo_pagina": "Título — Subtítulo para <title>/OG",
    "descricao": "1-2 frases para meta description",
    "og_desc": "1 frase de chamada para compartilhamento",
    "tese": "1 frase-tese que abre a página",
    "figura_dica": "instrução curta de uso da figura",
    "img_alt": "alt descritivo da imagem de fundo (faixa superior e inferior)",
    "dica_label": "rótulo curto da dica (ex.: 'Dica de Arquiteto')",
    "rodape": "frase de efeito de rodapé",
    "icone": "1 emoji",
    "cenario": "Caverna|Aldeia|Acampamento|Sala de Controle|Tribo|...",
    "cor": "#hex acento dominante",
    "cat": "arq|qual|dados|prod|seg",
    "nivel": "Iniciante|Intermediário|Avançado",
    "tags": ["3 a 4 conceitos-chave"],
    "desc": "1 linha para o card do Atlas"
  }},
  "ordem": ["id1", "id2", "... {n} ids em snake_case ..."],
  "conceitos": {{
    "id1": {{
      "zona": "Faixa/Região na metáfora",
      "titulo": "Conceito — Elemento da metáfora",
      "icone": "1 emoji",
      "cor": "#hex",
      "label": "rótulo curto p/ legenda",
      "metafora": "frase ligando o elemento da metáfora ao conceito técnico",
      "bullets": ["3 bullets acessíveis para devs juniores"],
      "ferramentas": [{{"nome": "Ferramenta real", "url": "https://..."}}],
      "dica": "1 dica prática acionável"
    }}
  }},
  "geo": {{ "id1": [left, top, width, height] }},
  "relacoes": {{ "id1": {{ "ids": ["id2","id3"], "nota": "como se conectam" }} }}
}}

Regras de GEO (em % do container): faixa superior top≈3-30 para 5 ids; faixa
inferior top≈54-75 para 7 ids; left distribuído 1→90; width 10-22; height 20-42.
Todos os ids de "ordem" devem existir em "conceitos", "geo" e (idealmente) "relacoes".
"""

CORRECAO_SUFIXO = """\

A tentativa anterior FALHOU na validação. Corrija EXATAMENTE estes erros e reemita o JSON completo:
{erros}
"""
