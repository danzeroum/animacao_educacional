// Componentes compartilhados da Forja.

export const NODES = [
  ['definir_slug', 'slug', '🏷️'],
  ['gerar_prompt', 'prompt', '💬'],
  ['gerar_imagem', 'imagem', '🖼️'],
  ['gerar_objeto', 'objeto', '🧩'],
  ['validar_objeto', 'validar', '✅'],
  ['atualizar_atlas', 'atlas', '🗺️'],
  ['deploy', 'deploy', '🚀'],
]

const RUN_DOT = { 'Em execução': 'running', 'Aguardando aprovação': 'wait',
  'Concluído': 'ok', 'Falha': 'fail' }

export const STATUS_COR = {
  ok: 'var(--ok)', running: 'var(--atencao)', wait: 'var(--info)',
  fail: 'var(--fail)', skip: 'var(--txt-fraco)', pending: 'var(--pending)',
}
const STATUS_LABEL = {
  ok: 'concluído', running: 'rodando…', wait: 'aguardando', fail: 'falhou',
  skip: 'pulado', pending: 'pendente',
}

export function StatusDot({ status }) {
  const s = status || 'pending'
  const pulse = s === 'running' || s === 'wait'
  return <span className={`dot ${s}${pulse ? ' pulse' : ''}`} />
}

export function RunStatus({ status }) {
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
      <span className={`dot ${RUN_DOT[status] || 'pending'}`} />{status}
    </span>
  )
}

// Trilha dos 7 nós do grafo (cards com borda-topo na cor do status).
export function GraphTrail({ nodes, tentativas }) {
  return (
    <div className="trail">
      {NODES.map(([id, label, icon], i) => {
        const st = nodes?.[id] || 'pending'
        const cor = STATUS_COR[st]
        const pulse = st === 'running' || st === 'wait'
        const objLabel = id === 'gerar_objeto' && tentativas > 1
          ? `tentativa ${tentativas}/3` : STATUS_LABEL[st]
        return (
          <div className="node-card" key={id} style={{ borderTopColor: cor }}>
            <div className="ntop">
              <span aria-hidden="true" style={{ fontSize: 16 }}>{icon}</span>
              <span className={`dot ${st}${pulse ? ' pulse' : ''}`} style={{ background: cor }} />
            </div>
            <div className="nname">{id}</div>
            <div className="nlabel" style={{ color: cor }}>{objLabel}</div>
            {i < NODES.length - 1 && <span className="arrow" aria-hidden="true">▶</span>}
          </div>
        )
      })}
    </div>
  )
}

export function Bar({ pct, cor }) {
  return <div className="bar"><i style={{ width: `${pct}%`, background: cor }} /></div>
}

export function Card({ title, children, style }) {
  return (
    <section className="card" style={style}>
      {title && <h3>{title}</h3>}
      {children}
    </section>
  )
}
