import { Card } from '../components.jsx'

const PROMPT_OBJETO = `EMITA APENAS UM JSON VÁLIDO (sem HTML, sem markdown):
{ metadados, ordem[12], conceitos{...}, geo{...}, relacoes{...} }
→ o Python injeta o JSON no template fixo (objeto.template.html).`

const CONTRATO_IMG = `Imagem 16:9, borda a borda. DUAS FAIXAS: 5 nichos em cima, 7 embaixo.
Nichos separados por PILARES de rocha. SEM TEXTO (só símbolos).`

const MARCADORES = `index.html (raiz): nova entrada antes de  /* __ATLAS_ENTRIES__ */
README.md (raiz): linha do catálogo antes de  <!-- __CATALOGO__ -->
Template base: backend/app/pipeline/templates/objeto.template.html
Seletor do validador: [data-conceito] dentro de #figura`

export default function PromptsTemplate() {
  return (
    <div className="grid" style={{ gap: 16 }}>
      <Card title="Prompt-fixo do objeto (A1 — só JSON)"><Bloco t={PROMPT_OBJETO} /></Card>
      <Card title="Contrato de composição da imagem"><Bloco t={CONTRATO_IMG} /></Card>
      <Card title="Marcadores-sentinela & template (A2 / A3)"><Bloco t={MARCADORES} /></Card>
    </div>
  )
}

function Bloco({ t }) {
  return (
    <pre className="mono" style={{ background: '#0c0703', padding: 14, borderRadius: 10,
      whiteSpace: 'pre-wrap', color: 'var(--txt-corpo-2)', margin: 0 }}>{t}</pre>
  )
}
