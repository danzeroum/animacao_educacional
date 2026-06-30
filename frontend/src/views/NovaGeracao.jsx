import { useMemo, useState } from 'react'
import { api } from '../lib/api.js'
import { Card } from '../components.jsx'

function slugify(tema, metafora) {
  return `${tema}-${metafora}`.toLowerCase().normalize('NFKD')
    .replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
}

const PASSOS = [
  '1. definir_slug — slug determinístico + pasta',
  '2. gerar_prompt — DeepSeek descreve a imagem (5+7 nichos)',
  '3. gerar_imagem — Gemini salva {slug}.png',
  '4. gerar_objeto — DeepSeek emite JSON → template fixo',
  '5. validar_objeto — Playwright (loop de autocorreção, máx. 3)',
  '6. atalas + deploy — atualiza Atlas e abre PR (após aprovação)',
]

export default function NovaGeracao({ go }) {
  const [tema, setTema] = useState('')
  const [metafora, setMetafora] = useState('')
  const [hitl, setHitl] = useState(true)
  const [tent, setTent] = useState(3)
  const [erro, setErro] = useState('')
  const [busy, setBusy] = useState(false)

  const slug = useMemo(() => (tema && metafora ? slugify(tema, metafora) : ''), [tema, metafora])

  async function iniciar() {
    setErro(''); setBusy(true)
    try {
      const { thread_id } = await api.criarRun(tema, metafora, Number(tent), hitl)
      go('console', thread_id)
    } catch (e) { setErro(String(e.message || e)) } finally { setBusy(false) }
  }

  return (
    <div className="grid" style={{ gridTemplateColumns: '1.2fr 1fr', alignItems: 'start' }}>
      <Card title="Parâmetros da geração">
        <label>Tema</label>
        <input value={tema} onChange={(e) => setTema(e.target.value)} placeholder="ex.: git flow" />
        <label>Metáfora</label>
        <input value={metafora} onChange={(e) => setMetafora(e.target.value)} placeholder="ex.: metrô" />

        <div style={{ marginTop: 14, padding: 12, border: '1px dashed var(--borda-media)', borderRadius: 10 }}>
          <div className="muted" style={{ fontSize: 12 }}>slug ao vivo</div>
          <div className="mono" style={{ color: 'var(--dourado)', fontSize: 14 }}>
            {slug || '—'}{slug && <span className="muted">  ·  imagem {slug}.png</span>}
          </div>
        </div>

        <div className="grid" style={{ gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          <div>
            <label>Modelo de texto</label>
            <select disabled><option>deepseek-chat</option></select>
          </div>
          <div>
            <label>Modelo de imagem</label>
            <select disabled><option>gemini-2.5-flash-image</option></select>
          </div>
        </div>

        <div className="grid" style={{ gridTemplateColumns: '1fr 1fr', gap: 12, alignItems: 'end' }}>
          <div>
            <label>Máx. tentativas</label>
            <input type="number" min={1} max={5} value={tent} onChange={(e) => setTent(e.target.value)} />
          </div>
          <label style={{ display: 'flex', gap: 8, alignItems: 'center', margin: '12px 0 9px' }}>
            <input type="checkbox" style={{ width: 'auto' }} checked={hitl}
              onChange={(e) => setHitl(e.target.checked)} />
            Aprovação humana (HITL)
          </label>
        </div>

        {erro && <p style={{ color: 'var(--fail)' }}>{erro}</p>}
        <button className="btn" style={{ marginTop: 14 }} disabled={!slug || busy} onClick={iniciar}>
          {busy ? 'Iniciando…' : '▶ Iniciar geração'}
        </button>
      </Card>

      <Card title="O que vai acontecer">
        <div className="grid" style={{ gap: 8 }}>
          {PASSOS.map((p) => (
            <div key={p} style={{ fontSize: 13, color: 'var(--txt-corpo-2)' }}>{p}</div>
          ))}
        </div>
      </Card>
    </div>
  )
}
