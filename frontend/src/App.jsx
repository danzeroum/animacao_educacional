import { useState } from 'react'
import Dashboard from './views/Dashboard.jsx'
import Execucoes from './views/Execucoes.jsx'
import NovaGeracao from './views/NovaGeracao.jsx'
import Console from './views/Console.jsx'
import Objetos from './views/Objetos.jsx'
import PullRequests from './views/PullRequests.jsx'
import ModelosChaves from './views/ModelosChaves.jsx'
import PromptsTemplate from './views/PromptsTemplate.jsx'
import Configuracoes from './views/Configuracoes.jsx'

const NAV = [
  { grupo: 'Execução', itens: [
    ['overview', 'Visão geral', '📊'],
    ['execucoes', 'Execuções', '🗂️'],
    ['nova', 'Nova geração', '✨'],
    ['console', 'Console', '🖥️'],
  ]},
  { grupo: 'Catálogo', itens: [
    ['objetos', 'Objetos', '🪨'],
    ['pulls', 'Pull Requests', '🔀'],
  ]},
  { grupo: 'Administração', itens: [
    ['modelos', 'Modelos & Chaves', '🔑'],
    ['prompts', 'Prompts & Template', '📝'],
    ['config', 'Configurações', '⚙️'],
  ]},
]

const TITULOS = {
  overview: ['Visão geral', 'Saúde do pipeline em um olhar'],
  execucoes: ['Execuções', 'Todos os runs do grafo'],
  nova: ['Nova geração', 'Dispare um objeto mapa-metáfora'],
  console: ['Console do run', 'Trilha do grafo ao vivo · aprovação'],
  objetos: ['Objetos', 'Catálogo gerado e integração com o Atlas'],
  pulls: ['Pull Requests', 'Branches abertas pelo deploy'],
  modelos: ['Modelos & Chaves', 'Provedores do pipeline'],
  prompts: ['Prompts & Template', 'Contratos que os nós cumprem'],
  config: ['Configurações', 'Servidor, checkpoint e deploy'],
}

export default function App() {
  const [view, setView] = useState('overview')
  const [activeRun, setActiveRun] = useState(null)

  // navegação central: trocar de tela; abrir um run leva ao Console.
  const go = (v, runId) => { if (runId !== undefined) setActiveRun(runId); setView(v) }

  const props = { go, activeRun, setActiveRun }
  const VIEWS = {
    overview: <Dashboard {...props} />,
    execucoes: <Execucoes {...props} />,
    nova: <NovaGeracao {...props} />,
    console: <Console {...props} />,
    objetos: <Objetos {...props} />,
    pulls: <PullRequests {...props} />,
    modelos: <ModelosChaves {...props} />,
    prompts: <PromptsTemplate {...props} />,
    config: <Configuracoes {...props} />,
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo-row">
          <span className="ic" aria-hidden="true">🔥</span>
          <div>
            <div className="logo">A Forja</div>
            <div className="logo-sub">pipeline · mapa-metáfora</div>
          </div>
        </div>
        {NAV.map((g) => (
          <div className="nav-group" key={g.grupo}>
            <h4>{g.grupo}</h4>
            {g.itens.map(([id, label, icon]) => (
              <button
                key={id}
                className={'nav-item' + (view === id ? ' ativo' : '')}
                onClick={() => go(id)}
                aria-current={view === id ? 'page' : undefined}
              >
                <span className="ic" aria-hidden="true">{icon}</span>{label}
              </button>
            ))}
          </div>
        ))}
        <div className="sidebar-foot">FastAPI · SSE · SQLite checkpoint<br />Deploy via git + PR (REST)</div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h1>{TITULOS[view][0]}</h1>
            <div className="sub">{TITULOS[view][1]}</div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <span className="repo">repo <b>animacao_educacional</b></span>
            <button className="btn" onClick={() => go('nova')}>✨ Nova geração</button>
          </div>
        </header>
        <div className="content">{VIEWS[view]}</div>
      </main>
    </div>
  )
}
