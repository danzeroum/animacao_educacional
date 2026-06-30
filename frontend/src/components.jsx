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

// Trilha dos 7 nós do grafo.
export function GraphTrail({ nodes, tentativas }) {
  return (
    <div className="trail">
      {NODES.map(([id, label, icon], i) => (
        <Frag key={id} last={i === NODES.length - 1}>
          <div className="node-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span aria-hidden="true">{icon}</span>
              <StatusDot status={nodes?.[id]} />
            </div>
            <div className="nname">{label}</div>
            <div className="nlabel">{id}</div>
            {id === 'gerar_objeto' && tentativas > 1 && (
              <div className="nlabel" style={{ color: 'var(--atencao)' }}>
                tentativa {tentativas}/3
              </div>
            )}
          </div>
        </Frag>
      ))}
    </div>
  )
}

function Frag({ children, last }) {
  return (
    <>
      {children}
      {!last && <span className="arrow" aria-hidden="true">▶</span>}
    </>
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
