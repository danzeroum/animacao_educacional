import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'
import { Card, Bar, RunStatus } from '../components.jsx'

const SAUDE = [
  ['slug', 100], ['prompt', 100], ['imagem', 94], ['objeto', 81],
  ['validar', 87], ['atlas', 100], ['deploy', 100],
]
const KPIS = [
  ['Execuções', '47', '+6 na semana'],
  ['Taxa de sucesso', '87%', 'últimos 30 runs'],
  ['Tentativas/run', '1.6', 'média'],
  ['PRs abertos', '3', 'aguardando merge'],
]

export default function Dashboard({ go }) {
  const [runs, setRuns] = useState([])
  const [prov, setProv] = useState(null)

  useEffect(() => {
    api.listarRuns().then((d) => setRuns(d.runs)).catch(() => {})
    api.providers().then(setProv).catch(() => {})
  }, [])

  return (
    <div className="grid" style={{ gap: 18 }}>
      <div className="grid" style={{ gridTemplateColumns: 'repeat(4,1fr)' }}>
        {KPIS.map(([t, v, s]) => (
          <Card key={t}>
            <div className="kicker">{t}</div>
            <div className="kpi">{v}</div>
            <div className="kpi-sub">{s}</div>
          </Card>
        ))}
      </div>

      <div className="grid" style={{ gridTemplateColumns: '1.4fr 1fr' }}>
        <Card title="Saúde do grafo · últimos 30 runs">
          <div className="grid" style={{ gap: 9 }}>
            {SAUDE.map(([n, p]) => (
              <div key={n} style={{ display: 'grid', gridTemplateColumns: '80px 1fr 38px', alignItems: 'center', gap: 10 }}>
                <span className="mono muted">{n}</span>
                <Bar pct={p} cor={p >= 90 ? 'var(--ok)' : 'var(--atencao)'} />
                <span className="mono" style={{ textAlign: 'right' }}>{p}%</span>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Cota das APIs">
          {prov ? (
            <div className="grid" style={{ gap: 14 }}>
              <Quota label="DeepSeek · grant"
                cur={`${prov.deepseek.grant_usado}M`} tot={`${prov.deepseek.grant_total}M`}
                pct={(prov.deepseek.grant_usado / prov.deepseek.grant_total) * 100} cor="var(--info)" />
              <Quota label="Gemini · imagens hoje"
                cur={prov.gemini.imagens_hoje} tot={prov.gemini.cota_diaria}
                pct={(prov.gemini.imagens_hoje / prov.gemini.cota_diaria) * 100} cor="var(--ok)" />
            </div>
          ) : <span className="muted">carregando…</span>}
        </Card>
      </div>

      <Card title="Execuções recentes">
        {runs.length === 0 && <span className="muted">Nenhum run ainda. Crie um em “Nova geração”.</span>}
        {runs.slice(0, 6).map((r) => (
          <button key={r.thread_id} className="nav-item" onClick={() => go('console', r.thread_id)}>
            <span className="mono" style={{ width: 200 }}>{r.slug}</span>
            <RunStatus status={r.status} />
          </button>
        ))}
      </Card>
    </div>
  )
}

function Quota({ label, cur, tot, pct, cor }) {
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
        <span className="muted" style={{ fontSize: 12 }}>{label}</span>
        <span className="mono">{cur}/{tot}</span>
      </div>
      <Bar pct={pct} cor={cor} />
    </div>
  )
}
