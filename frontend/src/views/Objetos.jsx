import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'

const COR = { 'No Atlas': 'var(--ok)', 'PR aberto': 'var(--atencao)',
  'Aguardando': 'var(--info)', 'Falha': 'var(--fail)' }

function pretty(slug) {
  return slug.split('-').map((w) => w[0]?.toUpperCase() + w.slice(1)).join(' ')
}

export default function Objetos() {
  const [d, setD] = useState(null)
  useEffect(() => { api.objetos().then(setD).catch(() => {}) }, [])
  if (!d) return <span className="muted">carregando…</span>

  return (
    <div className="grid" style={{ gap: 16 }}>
      <div style={{ fontSize: 13, color: 'var(--txt-mudo)' }}>
        Objetos gerados e seu estado de integração com o Atlas (
        <span style={{ color: 'var(--ok)' }}>{d.linkados} de {d.total} linkados</span>).
      </div>
      <div className="grid" style={{ gridTemplateColumns: 'repeat(3,1fr)', gap: 16 }}>
        {d.objetos.map((o) => {
          const cor = COR[o.status] || 'var(--pending)'
          return (
            <a key={o.slug} href={`/${o.slug}/index.html`} target="_blank" rel="noopener"
              style={{ textDecoration: 'none', border: '1px solid var(--borda-sutil)', borderTop: `3px solid ${cor}`,
                borderRadius: 13, background: 'linear-gradient(180deg, rgba(45,30,17,.7), rgba(20,13,7,.7))', padding: '15px 16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 9 }}>
                <span className="mono" style={{ fontSize: 11, color: 'var(--txt-mudo-2)' }}>{o.slug}</span>
                <span style={{ fontSize: 10.5, color: cor, display: 'inline-flex', alignItems: 'center', gap: 5 }}>
                  <span className="dot" style={{ width: 6, height: 6, background: cor }} />{o.status}
                </span>
              </div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: 16, fontWeight: 600, color: 'var(--txt-claro)' }}>
                {pretty(o.slug)}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 13,
                paddingTop: 11, borderTop: '1px solid rgba(109,91,71,.25)' }}>
                <span style={{ fontSize: 11.5, color: 'var(--txt-mudo-2)' }}>imagem {o.tem_imagem ? '✓' : '✕'}</span>
                <span style={{ fontFamily: 'var(--font-display)', fontSize: 11, color: cor }}>Abrir →</span>
              </div>
            </a>
          )
        })}
      </div>
    </div>
  )
}
