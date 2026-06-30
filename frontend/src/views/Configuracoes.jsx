import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'
import { Card } from '../components.jsx'

const ROTULOS = {
  servidor: 'Servidor', eventos: 'Eventos', checkpointer: 'Checkpointer',
  aprovacao_humana: 'Aprovação humana', max_tentativas: 'Máx. tentativas',
  padrao_branch: 'Padrão de branch', dry_run: 'Dry-run (sem publicar)',
  repo_root: 'Raiz do repositório',
}

export default function Configuracoes() {
  const [c, setC] = useState(null)
  useEffect(() => { api.config().then(setC).catch(() => {}) }, [])
  if (!c) return <span className="muted">carregando…</span>

  return (
    <Card title="Configurações">
      {Object.entries(ROTULOS).map(([k, label]) => (
        <div key={k} style={{ display: 'flex', justifyContent: 'space-between',
          padding: '10px 0', borderBottom: '1px solid var(--divisor)' }}>
          <span className="muted">{label}</span>
          <span className="mono" style={{ color: 'var(--txt-claro)' }}>{String(c[k])}</span>
        </div>
      ))}
      <button className="btn" style={{ marginTop: 16 }} disabled>Salvar</button>
    </Card>
  )
}
