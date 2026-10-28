import { startTransition, useState } from "react";
import { ESTUDO, SCALES, type PanelMode } from "./data/conteudo";
import { ScaleScene } from "./components/ScaleScene";
import { SidePanel } from "./components/SidePanel";

export default function App() {
  const [scaleIndex, setScaleIndex] = useState(3); // começa na célula
  const [mode, setMode] = useState<PanelMode>("contexto");
  const scale = SCALES[scaleIndex];

  const go = (next: number) => {
    startTransition(() => {
      setScaleIndex(Math.max(0, Math.min(SCALES.length - 1, next)));
    });
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-kicker">
            {ESTUDO.instituicao} · {ESTUDO.tipo}
          </div>
          <h1>{ESTUDO.titulo}</h1>
          <p>
            Do organismo ao átomo — exploração visual com painéis de bioinformática e
            quimioinformática para estudantes de biologia e química.
          </p>
        </div>
        <div className="mode-switch" role="group" aria-label="Modo do painel">
          {(
            [
              ["contexto", "Contexto"],
              ["bioinfo", "Bioinformática"],
              ["quimioinfo", "Quimioinformática"],
            ] as const
          ).map(([id, label]) => (
            <button
              key={id}
              type="button"
              aria-pressed={mode === id}
              onClick={() => setMode(id)}
            >
              {label}
            </button>
          ))}
        </div>
      </header>

      <main className="workspace">
        <section className="stage" aria-label="Palco de escalas">
          <nav className="scale-rail" aria-label="Níveis de escala">
            {SCALES.map((item, index) => (
              <button
                key={item.id}
                type="button"
                aria-current={index === scaleIndex}
                onClick={() => go(index)}
              >
                <strong>{item.titulo}</strong>
                <span>{item.escala}</span>
              </button>
            ))}
          </nav>

          <ScaleScene scaleId={scale.id} />
          <div className="stage-overlay" />

          <div className="zoom-controls">
            <button
              type="button"
              aria-label="Afastar (escala maior)"
              onClick={() => go(scaleIndex - 1)}
              disabled={scaleIndex === 0}
            >
              −
            </button>
            <button
              type="button"
              aria-label="Aproximar (escala menor)"
              onClick={() => go(scaleIndex + 1)}
              disabled={scaleIndex === SCALES.length - 1}
            >
              +
            </button>
          </div>
        </section>

        <SidePanel scale={scale} mode={mode} />
      </main>

      <footer className="footer">
        Pesquisa exploratória educacional · conectada ao portfólio{" "}
        <a href="https://github.com/HebertFelix/drug-discovery-workflows">
          drug-discovery-workflows
        </a>
        . HUD celular ilustrativo (ATS MATRIX · demonstração). Rode local com{" "}
        <code>npm run dev</code> em <code>atlas-escalas-senai/</code>.
      </footer>
    </div>
  );
}
