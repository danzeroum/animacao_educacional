import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'
import { Card, Bar } from '../components.jsx'

export default function ModelosChaves() {
  const [p, setP] = useState(null)
  useEffect(() => { api.providers().then(setP).catch(() => {}) }, [])
  if (!p) return <span className="muted">carregando…</span>

  return (
    <div className="grid" style={{ gridTemplateColumns: 'repeat(3,1fr)' }}>
      <Card title="DeepSeek">
        <Linha k="Chave" v={p.deepseek.configurado ? '•••• configurada' : 'ausente (.env)'} />
        <Linha k="Modelo" v={p.deepseek.model} />
        <Linha k="base_url" v={p.deepseek.base_url} />
        <div style={{ marginTop: 10 }}>
          <div className="muted" style={{ fontSize: 12 }}>grant {p.deepseek.grant_usado}M / {p.deepseek.grant_total}M</div>
          <Bar pct={(p.deepseek.grant_usado / p.deepseek.grant_total) * 100} cor="var(--info)" />
        </div>
      </Card>
      <Card title="Gemini (imagem)">
        <Linha k="Chave" v={p.gemini.configurado ? '•••• configurada' : 'ausente (.env)'} />
        <Linha k="Modelo" v={p.gemini.model} />
        <div style={{ marginTop: 10 }}>
          <div className="muted" style={{ fontSize: 12 }}>{p.gemini.imagens_hoje} / {p.gemini.cota_diaria} hoje</div>
          <Bar pct={(p.gemini.imagens_hoje / p.gemini.cota_diaria) * 100} cor="var(--ok)" />
        </div>
      </Card>
      <Card title="GitHub">
        <Linha k="Repo" v={p.github.repo} />
        <Linha k="Base" v={p.github.base} />
        <Linha k="Token" v={p.github.token ? '•••• configurado' : 'ausente (push-only)'} />
        <Linha k="Dry-run" v={p.github.dry_run ? 'ATIVO (não publica)' : 'desligado'} />
        <Linha k="Ação" v={p.github.acao} />
        <p className="muted" style={{ fontSize: 11.5, marginTop: 10 }}>
          Chaves vêm do <span className="mono">.env</span> — nunca commitadas.
        </p>
      </Card>
    </div>
  )
}

function Linha({ k, v }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid var(--divisor)' }}>
      <span className="muted" style={{ fontSize: 12 }}>{k}</span>
      <span className="mono" style={{ fontSize: 12 }}>{v}</span>
    </div>
  )
}
