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

// SSE com guard: dedupe por thread_id e fecho adiado, para que o double-invoke
// de efeitos do React StrictMode (dev) NÃO abra duas conexões. Retorna uma
// função de cancelamento (unsubscribe).
const _streams = new Map() // id -> { es, subs:Set, closeTimer }

export function streamRun(id, onNode) {
  let entry = _streams.get(id)
  if (entry?.closeTimer) { clearTimeout(entry.closeTimer); entry.closeTimer = null }
  if (!entry) {
    const es = new EventSource(`${BASE}/runs/${id}/stream`)
    entry = { es, subs: new Set(), closeTimer: null }
    es.addEventListener('node', (e) => {
      const data = JSON.parse(e.data)
      entry.subs.forEach((fn) => fn(data))
    })
    _streams.set(id, entry)
  }
  entry.subs.add(onNode)

  return () => {
    entry.subs.delete(onNode)
    if (entry.subs.size === 0) {
      // adia o fecho: se o StrictMode remontar logo em seguida, reaproveita.
      entry.closeTimer = setTimeout(() => {
        if (entry.subs.size === 0) { entry.es.close(); _streams.delete(id) }
      }, 150)
    }
  }
}
