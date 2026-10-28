import type { PanelMode, ScaleLevel } from "../data/conteudo";
import {
  BIOINFO_BY_SCALE,
  CELL_HUD,
  ESTUDO,
  QUIMIO_BY_SCALE,
} from "../data/conteudo";
import { MoleculePanel } from "./MoleculePanel";

interface Props {
  scale: ScaleLevel;
  mode: PanelMode;
}

export function SidePanel({ scale, mode }: Props) {
  const bio = BIOINFO_BY_SCALE[scale.id];
  const chem = QUIMIO_BY_SCALE[scale.id];

  return (
    <aside className="side-panel">
      <h2>{scale.titulo}</h2>
      <p className="meta">
        Escala {scale.escala} · {scale.resumo}
      </p>

      {mode === "contexto" && (
        <>
          <div className="card">
            <h3>Pergunta-guia</h3>
            <p style={{ margin: 0 }}>{scale.pergunta}</p>
          </div>
          <div className="card">
            <h3>Sobre este estudo</h3>
            <div className="kv">
              <div className="kv-row">
                <span>Instituição</span>
                <span>{ESTUDO.instituicao}</span>
              </div>
              <div className="kv-row">
                <span>Tipo</span>
                <span>{ESTUDO.tipo}</span>
              </div>
              <div className="kv-row">
                <span>Objetivo</span>
                <span>{ESTUDO.objetivo}</span>
              </div>
            </div>
            <p className="aviso">{ESTUDO.limites}</p>
          </div>
          {scale.id === "celula" && (
            <div className="card">
              <h3>Leitura do HUD (ilustrativo)</h3>
              <p style={{ marginTop: 0 }}>{CELL_HUD.nota}</p>
              <p style={{ marginBottom: 0, fontSize: "0.9rem" }}>
                Conectores dourados, mitocôndrias âmbar, rede nuclear, anel de RE e
                vesículas de vidro são metáforas visuais para orientar a exploração —
                não um laudo de imagem.
              </p>
            </div>
          )}
        </>
      )}

      {mode === "bioinfo" && (
        <div className="card">
          <h3>{bio?.titulo ?? "Bioinformática nesta escala"}</h3>
          {bio ? (
            <>
              <div className="kv">
                {bio.itens.map((item) => (
                  <div className="kv-row" key={item.rotulo}>
                    <span>{item.rotulo}</span>
                    <span>{item.valor}</span>
                  </div>
                ))}
              </div>
              {bio.sequencias?.map((seq) => (
                <div key={seq.tipo} style={{ marginTop: "0.8rem" }}>
                  <div style={{ fontSize: "0.85rem", marginBottom: "0.35rem" }}>{seq.tipo}</div>
                  <div className="seq">{seq.trecho}</div>
                  <p className="aviso">{seq.nota}</p>
                </div>
              ))}
              <p className="aviso">{bio.aviso}</p>
            </>
          ) : (
            <p>
              Nesta escala, a bioinformática aparece sobretudo como contexto (organismo,
              órgão, tecido). Avance até <strong>célula</strong>, <strong>organela</strong>{" "}
              ou <strong>molécula</strong> para painéis mais densos.
            </p>
          )}
        </div>
      )}

      {mode === "quimioinfo" && (
        <div className="card">
          <h3>{chem ? chem.nome : "Quimioinformática nesta escala"}</h3>
          {chem ? (
            <>
              <MoleculePanel card={chem} />
              <div className="kv" style={{ marginTop: "0.85rem" }}>
                <div className="kv-row">
                  <span>Fórmula</span>
                  <span>{chem.formula}</span>
                </div>
                <div className="kv-row">
                  <span>Massa molar</span>
                  <span>{chem.massaMolar}</span>
                </div>
                <div className="kv-row">
                  <span>Polaridade</span>
                  <span>{chem.polaridade}</span>
                </div>
                <div className="kv-row">
                  <span>Orbitais / ligações</span>
                  <span>{chem.orbitais}</span>
                </div>
                <div className="kv-row">
                  <span>Ligações</span>
                  <span>{chem.ligacoes.join(" · ")}</span>
                </div>
              </div>
              <div style={{ marginTop: "0.75rem" }}>
                <div style={{ fontSize: "0.85rem", marginBottom: "0.35rem" }}>SMILES</div>
                <div className="seq">{chem.smiles}</div>
              </div>
              <p className="aviso">{chem.aviso}</p>
            </>
          ) : (
            <p>
              A quimioinformática ganha detalhe nas escalas <strong>molécula</strong> e{" "}
              <strong>átomo</strong>. Use o zoom (− / +) para chegar lá.
            </p>
          )}
        </div>
      )}
    </aside>
  );
}
