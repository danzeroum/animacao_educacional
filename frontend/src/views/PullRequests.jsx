import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'
import { Card } from '../components.jsx'

export default function PullRequests() {
  const [pulls, setPulls] = useState([])
  useEffect(() => { api.pulls().then((d) => setPulls(d.pulls)).catch(() => {}) }, [])

  return (
    <Card title="Pull Requests">
      {pulls.length === 0 ? <span className="muted">Nenhum PR aberto ainda.</span> : (
        <table>
          <thead><tr><th>Slug</th><th>Branch</th><th>Status</th><th></th></tr></thead>
          <tbody>
            {pulls.map((p) => (
              <tr key={p.slug}>
                <td className="mono">{p.slug}</td>
                <td className="mono muted">{p.branch}</td>
                <td>{p.status}</td>
                <td><a href={p.url} target="_blank" rel="noopener" style={{ color: 'var(--info)' }}>GitHub ↗</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Card>
  )
}
