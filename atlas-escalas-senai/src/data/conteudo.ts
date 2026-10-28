export type ScaleId =
  | "organismo"
  | "orgao"
  | "tecido"
  | "celula"
  | "organela"
  | "molecula"
  | "atomo";

export type PanelMode = "contexto" | "bioinfo" | "quimioinfo";

export interface ScaleLevel {
  id: ScaleId;
  titulo: string;
  escala: string;
  resumo: string;
  pergunta: string;
  visualHint: string;
}

export interface BioinfoCard {
  titulo: string;
  itens: { rotulo: string; valor: string }[];
  sequencias?: { tipo: string; trecho: string; nota: string }[];
  aviso: string;
}

export interface QuimioinfoCard {
  nome: string;
  formula: string;
  massaMolar: string;
  polaridade: string;
  ligacoes: string[];
  orbitais: string;
  smiles: string;
  aviso: string;
}

export const SCALES: ScaleLevel[] = [
  {
    id: "organismo",
    titulo: "Organismo",
    escala: "~1–2 m",
    resumo: "Vista de partida: o corpo humano como sistema integrado.",
    pergunta: "Como uma mudança molecular pode ecoar até o organismo?",
    visualHint: "silhueta",
  },
  {
    id: "orgao",
    titulo: "Órgão",
    escala: "~cm",
    resumo: "Foco no coração como exemplo de órgão com demanda energética alta.",
    pergunta: "Por que mitocôndrias abundam em tecido cardíaco?",
    visualHint: "coracao",
  },
  {
    id: "tecido",
    titulo: "Tecido",
    escala: "~mm–µm",
    resumo: "Miocárdio: células musculares alinhadas e irrigadas.",
    pergunta: "Como a arquitetura do tecido condiciona a função?",
    visualHint: "fibras",
  },
  {
    id: "celula",
    titulo: "Célula",
    escala: "~10–100 µm",
    resumo: "Célula eucariótica com HUD ilustrativo (ATS MATRIX · estudo).",
    pergunta: "Quais contatos e organelas sustentam o metabolismo local?",
    visualHint: "celula",
  },
  {
    id: "organela",
    titulo: "Organela",
    escala: "~0,5–5 µm",
    resumo: "Mitocôndria: potencial de membrana e cadeia respiratória.",
    pergunta: "O que o ΔΨ mitocondrial indica sobre o estado energético?",
    visualHint: "mitocondria",
  },
  {
    id: "molecula",
    titulo: "Molécula",
    escala: "~nm",
    resumo: "ATP e glicose como moedas e combustíveis do metabolismo.",
    pergunta: "Como a estrutura química condiciona a função biológica?",
    visualHint: "molecula",
  },
  {
    id: "atomo",
    titulo: "Átomo",
    escala: "~Å / pm",
    resumo: "Núcleo e nuvem eletrônica: base da ligação química.",
    pergunta: "O que muda quando um elétron é compartilhado ou transferido?",
    visualHint: "atomo",
  },
];

export const CELL_HUD = {
  titulo: "ATS MATRIX // estudo ilustrativo",
  subtitulo: "Célula vermelha · três cantos · rede dourada · apenas HUD",
  metricas: [
    { rotulo: "Grânulos (ilustrativo)", valor: "6.425" },
    { rotulo: "Contatos registrados", valor: "> 25.000" },
    { rotulo: "Vesículas registradas", valor: "> 17.000" },
    { rotulo: "ΔV mitocondrial", valor: "≈ –145 a –163 mV" },
  ],
  ciclo:
    "TRUE → ÓSMIO → URANILA → CHUMBO → PRATA → CRIO",
  nota:
    "Os números sobre o vidro são demonstração didática. Esta interface não afirma ter gerado microscopia real; o HUD organiza leitura exploratória.",
};

export const BIOINFO_BY_SCALE: Partial<Record<ScaleId, BioinfoCard>> = {
  celula: {
    titulo: "Bioinformática · célula",
    itens: [
      { rotulo: "Modelo didático", valor: "Célula eucariótica animal" },
      { rotulo: "Genoma nuclear", valor: "~20 mil genes codificadores (humano, ordem de grandeza)" },
      { rotulo: "Transcriptoma", valor: "Expressão dependente de tecido e estímulo" },
      { rotulo: "Proteoma local", valor: "Membrana, citoesqueleto, organelas" },
    ],
    sequencias: [
      {
        tipo: "DNA (exemplo didático)",
        trecho: "ATGCGT…AAC",
        nota: "Trecho fictício para ensino de leitura 5'→3'.",
      },
    ],
    aviso:
      "Painel exploratório: não substitui curadoria UniProt/Ensembl para pesquisa formal.",
  },
  organela: {
    titulo: "Bioinformática · mitocôndria",
    itens: [
      { rotulo: "Genes mtDNA (humano)", valor: "13 proteínas + rRNA/tRNA" },
      { rotulo: "Cadeia respiratória", valor: "Complexos I–IV + ATP sintase" },
      { rotulo: "ΔΨ típico (ordem)", valor: "cerca de –150 mV (contexto celular)" },
      { rotulo: "Doenças associadas", valor: "Mutações mtDNA / nucleares (exemplo didático)" },
    ],
    sequencias: [
      {
        tipo: "Peptídeo sinal (ilustrativo)",
        trecho: "MLSLR…",
        nota: "Endereçamento mitocondrial — esquema de ensino.",
      },
    ],
    aviso:
      "ΔΨ e contagens do HUD são ilustrativos neste estudo SENAI; valide em literatura primária.",
  },
  molecula: {
    titulo: "Bioinformática · macromolécula",
    itens: [
      { rotulo: "Exemplo", valor: "Canal / enzima / transportador" },
      { rotulo: "Entrada estrutural", valor: "PDB (quando disponível)" },
      { rotulo: "Ligante", valor: "ATP, substrato ou inibidor" },
      { rotulo: "Próximo passo no portfólio", valor: "projects/02_target_evidence" },
    ],
    aviso:
      "Conecte esta escala aos workflows de evidência de alvo e docking do repositório.",
  },
};

export const QUIMIO_BY_SCALE: Partial<Record<ScaleId, QuimioinfoCard>> = {
  molecula: {
    nome: "Glicose (α-D-glucopiranose)",
    formula: "C₆H₁₂O₆",
    massaMolar: "180,16 g·mol⁻¹",
    polaridade: "Polar (múltiplas hidroxilas; solúvel em água)",
    ligacoes: ["C–C", "C–O", "O–H", "anel piranose"],
    orbitais: "Ligações σ (sp³) no esqueleto; pares isolados no oxigênio",
    smiles: "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
    aviso:
      "Modelo didático 2D/3D simplificado. Para descritores avançados, use o Projeto 03 (RDKit).",
  },
  atomo: {
    nome: "Carbono",
    formula: "C",
    massaMolar: "12,01 g·mol⁻¹",
    polaridade: "Não se aplica a átomo isolado da mesma forma que a molécula",
    ligacoes: ["até 4 ligações covalentes típicas"],
    orbitais: "2s² 2p² → hibridizações sp / sp² / sp³ em moléculas",
    smiles: "[C]",
    aviso: "Representação esquemática de núcleo + nuvem eletrônica para ensino.",
  },
};

export const ESTUDO = {
  instituicao: "SENAI",
  titulo: "Atlas de Escalas",
  tipo: "Estudo e pesquisa exploratória",
  autores: "Hebert Felix e colaboradores didáticos",
  objetivo:
    "Permitir que estudantes de biologia e química percorram, em zoom contínuo por níveis, o caminho organismo → átomo, conectando leitura visual a noções de bioinformática e quimioinformática.",
  limites:
    "Protótipo educacional. Dados de HUD celular são ilustrativos. Não é diagnóstico clínico nem microscopia certificada.",
};
