import { useEffect, useState } from 'react'
import { api, streamRun } from '../lib/api.js'
import { Card, GraphTrail, RunStatus } from '../components.jsx'

export default function Console({ activeRun, go }) {
  const [run, setRun] = useState(null)
  const [nodes, setNodes] = useState({})
  const [log, setLog] = useState([])
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    if (!activeRun) return
    let alive = true
    setLog([]); setNodes({})
    api.run(activeRun).then((d) => {
      if (!alive) return
      setRun(d); setNodes(d.nodes || {}); setLog(d.log || [])
    }).catch(() => {})

    // streamRun retorna um unsubscribe (conexão SSE deduplicada por thread_id).
    const unsubscribe = streamRun(activeRun, (ev) => {
      if (!alive) return
      if (ev.node === '_run') { api.run(activeRun).then(setRun).catch(() => {}); return }
      setNodes((n) => ({ ...n, [ev.node]: ev.status }))
      if (ev.message) setLog((l) => [...l, { ts: ev.ts, status: ev.status, message: ev.message }])
    })
    return () => { alive = false; unsubscribe() }
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

  const checks = run.checklist || []
  const okCount = checks.filter((c) => c.ok).length

  return (
    <div className="grid" style={{ gap: 20 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div className="mono" style={{ fontSize: 12.5, color: 'var(--dourado-3)' }}>
          run <span style={{ color: 'var(--txt-corpo-2)' }}>#{run.thread_id.slice(0, 4)}</span> · thread{' '}
          <span style={{ color: 'var(--txt-corpo-2)' }}>{run.slug}</span>
        </div>
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 7, fontFamily: 'var(--font-display)',
          fontSize: 11.5, padding: '7px 13px', borderRadius: 9, color: COR_PILL[run.status],
          border: `1px solid ${COR_PILL[run.status]}`,
          background: `color-mix(in srgb, ${COR_PILL[run.status]} 14%, transparent)` }}>
          {emExec && <span className="spin" />}<RunStatus status={run.status} />
        </span>
      </div>

      <GraphTrail nodes={nodes} tentativas={run.tentativas} />

      <div className="grid" style={{ gridTemplateColumns: '1.1fr .9fr', gap: 20, alignItems: 'start' }}>
        <div className="grid" style={{ gap: 16 }}>
          <section className="card" style={{ padding: '15px 16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 11 }}>
              <span style={{ fontFamily: 'var(--font-display)', fontSize: 12, color: 'var(--txt-corpo-2)' }}>
                validar_objeto · §4.4
              </span>
              {checks.length > 0 && (
                <span style={{ fontSize: 11.5, fontWeight: 600, color: okCount === checks.length ? 'var(--ok)' : 'var(--atencao)' }}>
                  {okCount} / {checks.length}{okCount === checks.length ? ' · aprovado' : ''}
                </span>
              )}
            </div>
            {checks.length === 0
              ? <span className="muted" style={{ fontSize: 12 }}>aguardando validação…</span>
              : (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '7px 16px' }}>
                  {checks.map((c) => (
                    <div key={c.label} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12, color: 'var(--txt-corpo)' }}>
                      <span style={{ width: 15, height: 15, borderRadius: 4, display: 'inline-flex',
                        alignItems: 'center', justifyContent: 'center', fontSize: 9,
                        background: `color-mix(in srgb, ${c.ok ? 'var(--ok)' : 'var(--fail)'} 22%, transparent)`,
                        color: c.ok ? 'var(--ok)' : 'var(--fail)' }}>{c.ok ? '✓' : '✕'}</span>
                      {c.label}
                    </div>
                  ))}
                </div>
              )}
            {run.tentativas > 1 && (
              <div style={{ marginTop: 10, fontSize: 11.5, color: 'var(--txt-mudo)', borderTop: '1px solid var(--divisor)', paddingTop: 9 }}>
                <span style={{ color: 'var(--atencao)' }}>↺ tentativa 1:</span> erro reinjetado → tentativa {run.tentativas} corrigiu.
              </div>
            )}
          </section>

          <div className="stream">
            <div className="titulo">stream de eventos</div>
            <div className="linhas">
              {log.map((e, i) => (
                <div key={i} className={`ev ${e.status}`}>
                  <span className="t">{new Date(e.ts).toLocaleTimeString()}</span>
                  <span className="m">{e.message}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {aguardando ? (
          <div className="hitl">
            <div className="head">
              <div className="t">⏸ Aprovação antes do deploy</div>
              <div style={{ fontSize: 12, color: 'var(--txt-corpo)', marginTop: 5, lineHeight: 1.5 }}>
                Pausa em <span className="mono" style={{ color: 'var(--info-2)' }}>interrupt_before=["deploy"]</span>.
              </div>
            </div>
            <div className="body">
              <div className="diff">
                {(run.payload?.diff || '').split('\n').map((l, i) => {
                  const sinal = l[0]
                  const cor = sinal === '+' ? 'var(--ok)' : sinal === '~' ? 'var(--atencao)' : 'var(--txt-mudo)'
                  return <div key={i}><span style={{ color: cor }}>{sinal}</span>{l.slice(1)}</div>
                })}
              </div>
              <div style={{ fontSize: 12, color: 'var(--txt-mudo)' }}>
                🌿 <span className="mono" style={{ color: 'var(--info-2)' }}>{run.payload?.branch}</span> → PR{' '}
                <span className="mono" style={{ color: 'var(--info-2)' }}>main</span>
              </div>
              <button className="btn azul" style={{ padding: 12 }} disabled={busy} onClick={() => act(api.aprovar)}>
                ✓ Aprovar e abrir Pull Request
              </button>
              <div style={{ display: 'flex', gap: 9 }}>
                <button className="btn sec" style={{ flex: 1, padding: 10 }} disabled={busy} onClick={() => act(api.regenerar)}>↺ Regenerar</button>
                <button className="btn perigo" style={{ flex: 1, padding: 10 }} disabled={busy} onClick={() => act(api.rejeitar)}>✕ Descartar</button>
              </div>
            </div>
          </div>
        ) : (
          <section className="card">
            {run.status === 'Concluído' && (
              <>
                <p style={{ color: 'var(--ok)', fontSize: 13 }}>✓ Concluído.</p>
                <p className="mono" style={{ fontSize: 12, color: 'var(--info-2)', wordBreak: 'break-all', margin: '8px 0' }}>
                  {run.payload?.pr_url}
                </p>
                <button className="btn sec" onClick={() => go('pulls')}>Ver Pull Requests</button>
              </>
            )}
            {emExec && <p className="muted" style={{ fontSize: 13 }}><span className="spin" /> Gerando…</p>}
            {falha && <p style={{ color: 'var(--fail)', fontSize: 13 }}>Falha após {run.tentativas} tentativas — deploy cancelado.</p>}
          </section>
        )}
      </div>
    </div>
  )
}

const COR_PILL = { 'Em execução': 'var(--atencao)', 'Aguardando aprovação': 'var(--info)',
  'Concluído': 'var(--ok)', 'Falha': 'var(--fail)' }
