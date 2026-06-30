import { useEffect, useRef, useState } from 'react'
import { api, streamRun } from '../lib/api.js'
import { Card, GraphTrail, RunStatus } from '../components.jsx'

export default function Console({ activeRun, go }) {
  const [run, setRun] = useState(null)
  const [nodes, setNodes] = useState({})
  const [log, setLog] = useState([])
  const [busy, setBusy] = useState(false)
  const esRef = useRef(null)

  useEffect(() => {
    if (!activeRun) return
    let alive = true
    setLog([]); setNodes({})
    api.run(activeRun).then((d) => {
      if (!alive) return
      setRun(d); setNodes(d.nodes || {}); setLog(d.log || [])
    }).catch(() => {})

    const es = streamRun(activeRun, (ev) => {
      if (ev.node === '_run') { api.run(activeRun).then(setRun).catch(() => {}); return }
      setNodes((n) => ({ ...n, [ev.node]: ev.status }))
      if (ev.message) setLog((l) => [...l, { ts: ev.ts, status: ev.status, message: ev.message }])
    })
    esRef.current = es
    return () => { alive = false; es.close() }
  }, [activeRun])

  async function act(fn) {
    setBusy(true)
    try { await fn(activeRun); const d = await api.run(activeRun); setRun(d); setNodes(d.nodes) }
    finally { setBusy(false) }
  }

  if (!activeRun) return <p className="muted">Selecione um run em “Execuções” ou crie um em “Nova geração”.</p>
  if (!run) return <p className="muted">carregando run…</p>

  const aguardando = run.status === 'Aguardando aprovação'
  const emExec = run.status === 'Em execução'
  const falha = run.status === 'Falha'

  return (
    <div className="grid" style={{ gap: 18 }}>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div className="kicker">run · thread</div>
            <div className="mono" style={{ fontSize: 15, color: 'var(--dourado)' }}>{run.slug}</div>
          </div>
          <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
            {emExec && <span className="spin" />}
            <RunStatus status={run.status} />
          </div>
        </div>
        <div style={{ marginTop: 16 }}>
          <GraphTrail nodes={nodes} tentativas={run.tentativas} />
        </div>
      </Card>

      <div className="grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
        <Card title="Validação §4.4">
          {(run.checklist || []).length === 0 && <span className="muted">aguardando validação…</span>}
          <div className="grid" style={{ gridTemplateColumns: '1fr 1fr', gap: 6 }}>
            {(run.checklist || []).map((c) => (
              <div key={c.label} style={{ fontSize: 12.5, color: c.ok ? 'var(--txt-corpo)' : 'var(--fail)' }}>
                {c.ok ? '✓' : '✕'} {c.label}
              </div>
            ))}
          </div>
          {run.tentativas > 1 && (
            <p className="muted" style={{ fontSize: 12, marginTop: 10 }}>
              loop: tentativa 1 falhou → erros reinjetados → tentativa {run.tentativas} corrigiu.
            </p>
          )}
        </Card>

        <Card title="Stream de eventos">
          <div className="stream">
            {log.map((e, i) => (
              <div key={i} className={`ev ${e.status}`}>
                <span className="t">{new Date(e.ts).toLocaleTimeString()}</span>
                <span className="m">{e.message}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {aguardando && (
        <div className="hitl">
          <h3 style={{ marginTop: 0, fontFamily: 'var(--font-display)', color: 'var(--info)' }}>
            🔎 Aprovação humana
          </h3>
          <p className="muted" style={{ fontSize: 13 }}>Revise os arquivos antes de publicar.</p>
          <pre className="mono" style={{ background: '#0c0703', padding: 12, borderRadius: 10, whiteSpace: 'pre-wrap' }}>
{run.payload?.diff || '—'}
          </pre>
          <p className="mono muted">branch: {run.payload?.branch} → main</p>
          <div style={{ display: 'flex', gap: 10, marginTop: 12 }}>
            <button className="btn azul" disabled={busy} onClick={() => act(api.aprovar).then(() => {})}>
              ✓ Aprovar e abrir Pull Request
            </button>
            <button className="btn sec" disabled={busy} onClick={() => act(api.regenerar)}>↻ Regenerar</button>
            <button className="btn sec" disabled={busy} onClick={() => act(api.rejeitar)}>✕ Descartar</button>
          </div>
        </div>
      )}

      {run.status === 'Concluído' && (
        <Card>
          <p style={{ color: 'var(--ok)' }}>✓ Concluído. PR: <a href={run.payload?.pr_url} target="_blank" rel="noopener" style={{ color: 'var(--info)' }}>{run.payload?.pr_url}</a></p>
          <button className="btn sec" onClick={() => go('pulls')}>Ver Pull Requests</button>
        </Card>
      )}

      {falha && (
        <Card>
          <p style={{ color: 'var(--fail)' }}>Falha após {run.tentativas} tentativas — deploy cancelado.</p>
        </Card>
      )}
    </div>
  )
}
