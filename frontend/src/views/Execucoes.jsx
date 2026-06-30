import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'
import { Card, RunStatus } from '../components.jsx'

const FILTROS = ['Todos', 'Aguardando aprovação', 'Em execução', 'Concluído', 'Falha']

export default function Execucoes({ go }) {
  const [runs, setRuns] = useState([])
  const [f, setF] = useState('Todos')

  useEffect(() => { api.listarRuns().then((d) => setRuns(d.runs)).catch(() => {}) }, [])
  const lista = runs.filter((r) => f === 'Todos' || r.status === f)

  return (
    <Card title="Execuções">
      <div style={{ display: 'flex', gap: 8, marginBottom: 14, flexWrap: 'wrap' }}>
        {FILTROS.map((x) => (
          <button key={x} className={'chip' + (f === x ? ' on' : '')} onClick={() => setF(x)}>{x}</button>
        ))}
      </div>
      {lista.length === 0 ? <span className="muted">Nenhum run.</span> : (
        <table>
          <thead><tr><th>Slug</th><th>Tema · Metáfora</th><th>Status</th><th>Tentativas</th><th></th></tr></thead>
          <tbody>
            {lista.map((r) => (
              <tr key={r.thread_id}>
                <td className="mono">{r.slug}</td>
                <td>{r.tema} · {r.metafora}</td>
                <td><RunStatus status={r.status} /></td>
                <td className="mono">{r.tentativas}/{r.max_tentativas}</td>
                <td><button className="btn sec" onClick={() => go('console', r.thread_id)}>Abrir</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Card>
  )
}
