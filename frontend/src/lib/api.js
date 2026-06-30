// Cliente HTTP da API da Forja (proxied em /api → :8000).
const BASE = '/api'

async function j(method, path, body) {
  const r = await fetch(BASE + path, {
    method,
    headers: body ? { 'content-type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!r.ok) throw new Error((await r.text()) || r.statusText)
  return r.json()
}

export const api = {
  criarRun: (tema, metafora, max_tentativas, hitl) =>
    j('POST', '/runs', { tema, metafora, max_tentativas, hitl }),
  listarRuns: () => j('GET', '/runs'),
  run: (id) => j('GET', `/runs/${id}`),
  aprovar: (id) => j('POST', `/runs/${id}/approve`),
  rejeitar: (id) => j('POST', `/runs/${id}/reject`),
  regenerar: (id) => j('POST', `/runs/${id}/regenerate`),
  objetos: () => j('GET', '/objects'),
  pulls: () => j('GET', '/pulls'),
  providers: () => j('GET', '/providers'),
  config: () => j('GET', '/config'),
}

// SSE: retorna o EventSource; o caller assina 'node'/'ping'.
export function streamRun(id, onNode) {
  const es = new EventSource(`${BASE}/runs/${id}/stream`)
  es.addEventListener('node', (e) => onNode(JSON.parse(e.data)))
  return es
}
