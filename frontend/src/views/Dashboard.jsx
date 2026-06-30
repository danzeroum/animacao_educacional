import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'
import { Bar } from '../components.jsx'

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
const COR_RUN = { 'Em execução': 'var(--atencao)', 'Aguardando aprovação': 'var(--info)',
  'Concluído': 'var(--ok)', 'Falha': 'var(--fail)' }

export default function Dashboard({ go }) {
  const [runs, setRuns] = useState([])
  const [prov, setProv] = useState(null)

  useEffect(() => {
    api.listarRuns().then((d) => setRuns(d.runs)).catch(() => {})
    api.providers().then(setProv).catch(() => {})
  }, [])

  return (
    <div className="grid" style={{ gap: 20 }}>
      <div className="grid" style={{ gridTemplateColumns: 'repeat(4,1fr)', gap: 16 }}>
        {KPIS.map(([t, v, s]) => (
          <div className="kpi-card" key={t}>
            <div className="kicker" style={{ fontSize: 11 }}>{t}</div>
            <div className="kpi">{v}</div>
            <div className="kpi-sub">{s}</div>
          </div>
        ))}
      </div>

      <div className="grid" style={{ gridTemplateColumns: '1.5fr 1fr', gap: 20 }}>
        <section className="card">
          <h3>Saúde do grafo · últimos 30 runs</h3>
          <div style={{ display: 'flex', gap: 12 }}>
            {SAUDE.map(([n, p]) => {
              const cor = p >= 90 ? 'var(--ok)' : 'var(--atencao)'
              return (
                <div key={n} style={{ flex: 1, textAlign: 'center' }}>
                  <div style={{ height: 64, display: 'flex', alignItems: 'flex-end', justifyContent: 'center' }}>
                    <div style={{ width: '70%', height: `${p}%`, borderRadius: '4px 4px 0 0',
                      background: `linear-gradient(180deg, ${cor}, color-mix(in srgb, ${cor} 30%, transparent))` }} />
                  </div>
                  <div className="mono" style={{ fontSize: 9, color: 'var(--txt-mudo-2)', marginTop: 6 }}>{n}</div>
                  <div style={{ fontSize: 10.5, color: cor, fontWeight: 600 }}>{p}%</div>
                </div>
              )
            })}
          </div>
        </section>

        <section className="card">
          <h3>Cota das APIs (grátis)</h3>
          {prov ? (
            <>
              <Quota nome="DeepSeek · grant" txt={`${prov.deepseek.grant_usado}M / ${prov.deepseek.grant_total}M`}
                pct={(prov.deepseek.grant_usado / prov.deepseek.grant_total) * 100} cor="var(--info)" />
              <Quota nome="Gemini · imagens hoje" txt={`${prov.gemini.imagens_hoje} / ${prov.gemini.cota_diaria}`}
                pct={(prov.gemini.imagens_hoje / prov.gemini.cota_diaria) * 100} cor="var(--ok)" />
              <div style={{ fontSize: 11, color: 'var(--txt-fraco)', lineHeight: 1.5, marginTop: 4 }}>
                DeepSeek: grant único de signup. Gemini: cota diária do free tier.
                Guardrail interrompe o run se a cota acabar.
              </div>
            </>
          ) : <span className="muted">carregando…</span>}
        </section>
      </div>

      <section className="card" style={{ padding: '6px 4px' }}>
        <div className="kicker" style={{ fontSize: 12, padding: '12px 16px 8px' }}>Execuções recentes</div>
        {runs.length === 0 && <div style={{ padding: '4px 16px 12px' }} className="muted">
          Nenhum run ainda. Crie um em “Nova geração”.</div>}
        {runs.slice(0, 6).map((r) => (
          <button key={r.thread_id} onClick={() => go('console', r.thread_id)}
            style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr auto', alignItems: 'center', gap: 14,
              width: '100%', textAlign: 'left', cursor: 'pointer', background: 'transparent', border: 'none',
              borderTop: '1px solid var(--divisor)', padding: '11px 16px' }}>
            <span className="cel-slug">{r.slug}</span>
            <span style={{ fontSize: 12, color: 'var(--txt-mudo)' }}>{r.tema} · {r.metafora}</span>
            <span style={{ fontSize: 11.5, color: COR_RUN[r.status], display: 'inline-flex', alignItems: 'center', gap: 6 }}>
              <span className="dot" style={{ background: COR_RUN[r.status] }} />{r.status}
            </span>
          </button>
        ))}
      </section>
    </div>
  )
}

function Quota({ nome, txt, pct, cor }) {
  return (
    <div style={{ marginBottom: 15 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12.5, color: 'var(--txt-corpo)', marginBottom: 6 }}>
        <span>{nome}</span><span className="muted">{txt}</span>
      </div>
      <Bar pct={pct} cor={cor} />
    </div>
  )
}
