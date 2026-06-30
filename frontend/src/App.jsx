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
  overview: 'Visão geral', execucoes: 'Execuções', nova: 'Nova geração',
  console: 'Console do run', objetos: 'Objetos', pulls: 'Pull Requests',
  modelos: 'Modelos & Chaves', prompts: 'Prompts & Template', config: 'Configurações',
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
        <div className="logo">🔥 A Forja</div>
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
                <span aria-hidden="true">{icon}</span>{label}
              </button>
            ))}
          </div>
        ))}
      </aside>

      <main className="main">
        <header className="topbar">
          <h1>{TITULOS[view]}</h1>
          <button className="btn" onClick={() => go('nova')}>✨ Nova geração</button>
        </header>
        <div className="content">{VIEWS[view]}</div>
      </main>
    </div>
  )
}
