import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'
import { Card } from '../components.jsx'

const COR = { 'No Atlas': 'var(--ok)', 'PR aberto': 'var(--atencao)',
  'Aguardando': 'var(--info)', 'Falha': 'var(--fail)' }

export default function Objetos() {
  const [d, setD] = useState(null)
  useEffect(() => { api.objetos().then(setD).catch(() => {}) }, [])
  if (!d) return <span className="muted">carregando…</span>

  return (
    <div className="grid" style={{ gap: 16 }}>
      <div className="kicker">{d.linkados} de {d.total} linkados no Atlas</div>
      <div className="grid" style={{ gridTemplateColumns: 'repeat(3,1fr)' }}>
        {d.objetos.map((o) => (
          <Card key={o.slug}>
            <div className="mono" style={{ color: 'var(--dourado)' }}>{o.slug}</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, margin: '8px 0' }}>
              <span className="dot" style={{ background: COR[o.status] || 'var(--pending)' }} />
              <span style={{ fontSize: 12 }}>{o.status}</span>
            </div>
            <div className="muted" style={{ fontSize: 12 }}>
              imagem: {o.tem_imagem ? '✓' : '✕'}
            </div>
            <a href={`/${o.slug}/index.html`} target="_blank" rel="noopener"
               style={{ color: 'var(--info)', fontSize: 13 }}>Abrir →</a>
          </Card>
        ))}
      </div>
    </div>
  )
}
